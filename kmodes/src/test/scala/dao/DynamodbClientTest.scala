package dao

import constants.VoteDecision.{Aye, No, NoAttend, VoteDecision}
import dao.DynamodbClientTest.createVotes
import dao.helpers.DataFactory
import model.{MPWithVotes, VotePair}
import org.mockito.ArgumentMatchers.any
import org.mockito.MockitoSugar.{mock, when}
import org.scalatest.flatspec.AnyFlatSpec
import service.DynamodbVotesFetcher

object DynamodbClientTest {
  def createVotes(votes: Seq[VoteDecision]): Seq[VotePair] = {
    for {
      (vote, i) <- votes.zipWithIndex
    } yield VotePair(i + 1, vote)
  }
}

class DynamodbClientTest extends AnyFlatSpec {


  "A votePair" should "be created" in {
    // given
    val votesOne = createVotes(Seq(No, NoAttend, Aye))
    val mpWithVotesOne = MPWithVotes(1, "Mr B Limond", "SNP", votesOne)

    val votesTwo = createVotes(Seq(No, No, NoAttend))
    val mpWithVoteTwo = MPWithVotes(2, "Teddy R", "Tories", votesTwo)

    val items = DataFactory.getItems(Seq(mpWithVotesOne, mpWithVoteTwo))

    val mockedDynamodbClient = mock[DynamodbClientTrait]
    val votesFetcher = new DynamodbVotesFetcher(mockedDynamodbClient)
    
    // when
    when(mockedDynamodbClient.scan(any, any)) thenReturn items
    val votesResult = votesFetcher.getVotes(2019)

    // then
    assert(votesResult.length == 2)
    assert(votesResult(0).votes == votesOne)
    assert(votesResult(1).votes == votesTwo)
  }

}
