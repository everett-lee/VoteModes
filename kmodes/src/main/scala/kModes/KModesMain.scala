package kModes

import model.{MP, MPWithVotes, VotePair}

class KModesMain(centroidsHelper: CentroidsHelper[Vector[MPWithVotes], List[VotePair]]) extends KModes[Vector[MPWithVotes]] {

  override def compute(MPsWithVotes: Vector[MPWithVotes]): Map[Int, MP] = ???
}

object KModesMain {
  def apply(centroidsHelper: CentroidsHelper[Vector[MPWithVotes], List[VotePair]] = new CentroidsHelperMain()): KModesMain = {
    new KModesMain(centroidsHelper)
  }
}