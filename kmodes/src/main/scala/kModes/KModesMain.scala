package kModes

import model.{MP, MPWithVotes, VotePair}

import scala.annotation.tailrec

class KModesMain extends KModes {
  val randomGenerator = scala.util.Random

  def initCentroids(MPsWithVotes: Vector[MPWithVotes], k: Int): Vector[MPWithVotes] = {
    require(k <= MPsWithVotes.size)

    val maxIndex = MPsWithVotes.size - 1
    (0 until k)
      .map(n => randomGenerator.nextInt(maxIndex))
      .map(index => MPsWithVotes(index))
      .to(Vector)
  }

  @tailrec
  final def calculateDistance(votes: List[VotePair], centroid: List[VotePair], acc: Int = 0): Int = {
    require(votes.size == centroid.size)

    votes match {
      case Nil => 0 + acc
      case x :: xs => {
        val res = if (x.voteDecision != centroid.head.voteDecision) 1 else 0
        calculateDistance(xs, centroid.tail, acc + res)
      }
    }
  }

  override def compute(MPsWithVotes: Vector[MPWithVotes]): Map[Int, MP] = ???
}
