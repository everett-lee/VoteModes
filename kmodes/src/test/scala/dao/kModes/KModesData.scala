package dao.kModes

import constants.VoteDecision.{Aye, No, NoAttend}
import model.{MPWithVotes, VotePair}

object KModesData {
  val votesOne = List(VotePair(1, Aye), VotePair(2, No), VotePair(3, NoAttend), VotePair(4, Aye), VotePair(5, No))
  val votesTwo = List(VotePair(1, Aye), VotePair(2, NoAttend), VotePair(3, No), VotePair(4, NoAttend), VotePair(5, NoAttend))
  val votesThree = List(VotePair(1, No), VotePair(2, No), VotePair(3, Aye), VotePair(4, No), VotePair(5, No))
  val votesFour = List(VotePair(1, Aye), VotePair(2, Aye), VotePair(3, Aye), VotePair(4, NoAttend), VotePair(5, Aye))
  val votesFive = List(VotePair(1, NoAttend), VotePair(2, NoAttend), VotePair(3, No), VotePair(4, NoAttend), VotePair(5, NoAttend))
  val votesSix = List(VotePair(1, No), VotePair(2, No), VotePair(3, No), VotePair(4, Aye), VotePair(5, NoAttend))
  val votesSeven = List(VotePair(1, NoAttend), VotePair(2, Aye), VotePair(3, Aye), VotePair(4, Aye), VotePair(5, Aye))
  val votesEight = List(VotePair(1, No), VotePair(2, No), VotePair(3, No), VotePair(4, Aye), VotePair(5, NoAttend))

  val MPs = Vector(MPWithVotes(0, "Mark E Smith", "The Fall", votesOne),
    MPWithVotes(1, "Richard D James", "Aphex", votesTwo),
    MPWithVotes(2, "Mark K", "Sun Kil Moon", votesThree),
    MPWithVotes(3, "Mason Mount", "Chael Sea", votesFour),
    MPWithVotes(4, "A Allen", "Trimley", votesFive),
    MPWithVotes(5, "T Werner", "Just Wide", votesSix),
    MPWithVotes(6, "SP Morrissey", "Controversial", votesSeven),
    MPWithVotes(7, "The last one", "Has band", votesEight),
  )

  val centroids = Vector(MPs(6), MPs(4), MPs(7))
}
