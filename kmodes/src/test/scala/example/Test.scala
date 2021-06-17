package example

import constants.VoteDecision
import dao.helpers.DataFactory
import model.{MPWithVotes, VotePair}
import org.scalatest.flatspec.AnyFlatSpec

class Test extends AnyFlatSpec  {

  "A votePair" should "be created" in {
    val voteOne = VotePair(1, VoteDecision.No)
    val voteTwo = VotePair(2, VoteDecision.NoAttend)
    val voteThree = VotePair(3, VoteDecision.Aye)

    val votesOne = Seq(voteOne, voteTwo, voteThree)
    val mpWithVotesOne = MPWithVotes(1, "Mr Limmond", votesOne)

    val voteFour = VotePair(1, VoteDecision.Aye)
    val voteFive = VotePair(2, VoteDecision.Aye)
    val voteSix = VotePair(3, VoteDecision.NoAttend)

    val votesTwo = Seq(voteFour, voteFive, voteSix)
    val mpWithVoteTwo = MPWithVotes(2, "Teddy R", votesTwo)

    val res = DataFactory.getItems(Seq(mpWithVotesOne, mpWithVoteTwo))
    println(res)
  }

}
