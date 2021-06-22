package kModes

import model.{MP, MPWithVotes, VotePair}

import scala.annotation.tailrec

class KModesMain extends KModes {
  val randomGenerator = scala.util.Random

  def initCentroids(MPsWithVotes: Vector[MPWithVotes], K: Int): Vector[MPWithVotes] = {
    require(K <= MPsWithVotes.size, f"K:$K%d is greater than input vector size")

    (0 until K)
      .map(n => randomGenerator.nextInt(MPsWithVotes.size))
      .map(index => MPsWithVotes(index))
      .to(Vector)
  }

  @tailrec
  final def calculateDistance(votes: List[VotePair], centroid: List[VotePair], acc: Int = 0): Int = {
    require(votes.size == centroid.size, "Vote sizes must match")

    votes match {
      case Nil => acc
      case x :: xs =>
        require(x.divisionId == centroid.head.divisionId, "Divisions Ids must match")
        val res = if (x.voteDecision != centroid.head.voteDecision) 1 else 0
        calculateDistance(xs, centroid.tail, acc + res)
    }
  }

  override def compute(MPsWithVotes: Vector[MPWithVotes]): Map[Int, MP] = ???
}
