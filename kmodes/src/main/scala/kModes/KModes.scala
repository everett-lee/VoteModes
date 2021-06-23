package kModes

import model.{MP}

trait KModes[A <: Seq[MP]] {
  def compute(MPsWithVotes: A): Map[Int, MP]
}
