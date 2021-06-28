package kModes

import model.{MPDetails, MPWithVotes, VotePair}

import scala.annotation.tailrec

class KModesMain(centroidsHelper: CentroidsHelper[Vector[MPWithVotes], List[VotePair]])
  extends KModes[Vector[MPWithVotes], Vector[MPDetails]] {
  private val K = 4
  private val MAX_ITERATIONS = 1000
  private var lastClusters: Map[Int, Vector[MPWithVotes]] = Map()

  @tailrec
  final private def looper(inMps: Vector[MPWithVotes], inCentroids: Vector[MPWithVotes], iteration: Int): Vector[MPWithVotes] = {
    // log iteration
    if (iteration >= MAX_ITERATIONS) {
      return inCentroids
    }

    val groupedByCentroid = centroidsHelper.groupByCentroid(inMps, inCentroids)
    if (groupedByCentroid == lastClusters) {
      return inCentroids
      // log reason for exit
    }
    lastClusters = groupedByCentroid

    val newCentroids = (for {
      (centroidIndex, mpsWithVotes) <- groupedByCentroid
    } yield centroidsHelper.calculateCentroid(mpsWithVotes, centroidIndex)).toVector
    // log new centroids

    looper(inMps, newCentroids, iteration + 1)
  }

  override def compute(mpsWithVotes: Vector[MPWithVotes]): Map[Int, Vector[MPDetails]] = {
    val initCentroids = centroidsHelper.initCentroids(mpsWithVotes, K)
    val finalCentroids = looper(mpsWithVotes, initCentroids, 0)

    centroidsHelper.groupByCentroid(mpsWithVotes, finalCentroids).view
      .mapValues(mpsWithVotes => mpsWithVotes
        .map(mpWithVotes => MPDetails(mpWithVotes.id, mpWithVotes.mpName, mpWithVotes.mpParty)))
      .toMap
    // log result

  }
}

object KModesMain {
  def apply(centroidsHelper: CentroidsHelper[Vector[MPWithVotes], List[VotePair]] = new CentroidsHelperMain()): KModesMain = {
    new KModesMain(centroidsHelper)
  }
}