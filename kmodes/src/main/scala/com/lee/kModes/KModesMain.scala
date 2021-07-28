package com.lee.kModes

import com.lee.constants.Constants
import com.lee.kModes.KModesMain.getEnvironmentVarOrDefault
import com.lee.model.{MPDetails, MPWithVotes, VotePair}
import com.typesafe.scalalogging.Logger

import scala.annotation.tailrec

class KModesMain(centroidsHelper: CentroidsHelper[Vector[MPWithVotes], List[VotePair]])
  extends KModes[Vector[MPWithVotes], Vector[MPDetails]] {
  val K: Int = getEnvironmentVarOrDefault("K_VALUE", 3)
  private val MAX_ITERATIONS = getEnvironmentVarOrDefault("MAX_ITERATIONS", 100)
  private var lastClusters: Map[Int, Vector[MPWithVotes]] = Map()
  val logger: Logger = Logger(Constants.loggerName)

  @tailrec
  final private def looper(inMps: Vector[MPWithVotes], inCentroids: Vector[MPWithVotes], iteration: Int): Vector[MPWithVotes] = {
    logger.info("K modes iteration: {}", iteration)
    if (iteration >= MAX_ITERATIONS) {
      return inCentroids
    }

    val groupedByCentroid = centroidsHelper.groupByCentroid(inMps, inCentroids)
    if (groupedByCentroid == lastClusters) {
      logger.info("Exiting K modes as clusters stable")
      return inCentroids
    }
    lastClusters = groupedByCentroid

    val newCentroids = (for {
      (centroidIndex, mpsWithVotes) <- groupedByCentroid
    } yield centroidsHelper.calculateCentroid(mpsWithVotes, centroidIndex)).toVector
    logger.info("New centroids: {}", newCentroids)

    looper(inMps, newCentroids, iteration + 1)
  }

  override def compute(mpsWithVotes: Vector[MPWithVotes]): Map[Int, Vector[MPDetails]] = {
    val initCentroids = centroidsHelper.initCentroids(mpsWithVotes, K)
    val finalCentroids = looper(mpsWithVotes, initCentroids, 0)

    val result = centroidsHelper.groupByCentroid(mpsWithVotes, finalCentroids)
      .mapValues(mpsWithVotes => mpsWithVotes
        .map(mpWithVotes => MPDetails(mpWithVotes.id, mpWithVotes.mpName, mpWithVotes.mpParty)))
    logger.info("Result {}", result)
    result
  }
}

object KModesMain {
  def apply(centroidsHelper: CentroidsHelper[Vector[MPWithVotes], List[VotePair]] = new CentroidsHelperMain()): KModesMain = {
    new KModesMain(centroidsHelper)
  }

  def getEnvironmentVarOrDefault(key: String, default: Int): Int = {
    if (System.getenv().containsKey(key)) sys.env(key).toInt else default;
  }
}