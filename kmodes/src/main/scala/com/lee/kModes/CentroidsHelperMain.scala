package com.lee.kModes
import com.lee.model.{MPWithVotes, VotePair}

import scala.annotation.tailrec

class CentroidsHelperMain extends CentroidsHelper[Vector[MPWithVotes], List[VotePair]] {
  override def initCentroids(MPsWithVotes: Vector[MPWithVotes], K: Int): Vector[MPWithVotes] = {
    (0 until K)
      .map(n => randomGenerator.nextInt(MPsWithVotes.size))
      .map(index => MPsWithVotes(index))
      .toVector
  }

  @tailrec
  final override def calculateDistance(votes: List[VotePair], centroid: List[VotePair], acc: Int = 0): Int = {
    require(votes.size == centroid.size, "Vote sizes must match")

    votes match {
      case Nil => acc
      case x :: xs =>
        require(x.divisionId == centroid.head.divisionId, "Divisions Ids must match")
        val res = if (x.voteDecision != centroid.head.voteDecision) 1 else 0
        calculateDistance(xs, centroid.tail, acc + res)
    }
  }

  override def calculateClosestCentroid(MPWithVotes: MPWithVotes, centroids: Vector[MPWithVotes]): Int = {
    centroids
      .map(centroid => (centroid, calculateDistance(MPWithVotes.votes, centroid.votes)))
      .minBy(_._2)._1.id // the id of the closest centroid
  }

  override def groupByCentroid(MPsWithVotes: Vector[MPWithVotes],
                      centroids: Vector[MPWithVotes]): Map[Int, Vector[MPWithVotes]] = {

    MPsWithVotes.groupBy(mp => calculateClosestCentroid(mp, centroids))
  }

  override def calculateCentroid(mpsWithVotes: Vector[MPWithVotes], centroidId: Int): MPWithVotes = {

    @tailrec
    def recursiveHelper(votes: List[List[VotePair]], res: List[VotePair]): List[VotePair] = {
      votes.head match {
        case Nil => res
        case x :: xs => {
          val heads = votes.map(inList => inList.head)
          val tails = votes.map(inList => inList.tail)
          val mode = heads.groupBy(identity)
            .maxBy({
              case (votePair, votes) =>
                votes.size + votePair.voteDecision.toString.length / 100.0 // add this as a tiebreaker
            })._1

          recursiveHelper(tails, mode :: res)
        }
      }
    }

    val votes = mpsWithVotes.map(mp => mp.votes).toList
    val centroidVotes = recursiveHelper(votes, List())
    MPWithVotes(centroidId, "","", centroidVotes.reverse)
  }


}
