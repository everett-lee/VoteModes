package kModes

import model.{MP, MPWithVotes}

class KModesMain extends KModes[Vector[MPWithVotes]] {

  override def compute(MPsWithVotes: Vector[MPWithVotes]): Map[Int, MP] = ???
}
