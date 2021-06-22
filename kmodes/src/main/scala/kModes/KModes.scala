package kModes

import model.{MP, MPWithVotes}

trait KModes {
  def compute(MPsWithVotes: Vector[MPWithVotes]): Map[Int, MP]
}
