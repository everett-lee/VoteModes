package com.lee.service

import com.lee.constants.VoteDecision.{Aye, No, NoAttend, VoteDecision}
import com.lee.aws.DynamodbClientTrait
import com.lee.helpers.DataFactory
import com.lee.model.{MPWithVotes, VotePair}
import org.mockito.ArgumentMatchers.any
import org.mockito.MockitoSugar.{mock, when}
import org.scalatest.wordspec.AnyWordSpec
import com.lee.service.DynamodbVotesFetcherTest.createVotes

object DynamodbVotesFetcherTest {
  def createVotes(votes: Seq[VoteDecision]): List[VotePair] = {
    for {
      (vote, i) <- votes.zipWithIndex
    } yield VotePair(i + 1, vote)
  }.toList
}

class DynamodbVotesFetcherTest extends AnyWordSpec {

  "A DynamodbVotesFetcher" should {
    "Create a collection of MPWithVotes" in {
      // given
      val votesOne = createVotes(Seq(No, NoAttend, Aye))
      val mpWithVotesOne = MPWithVotes(1, "Mr B Limond", "SNP", votesOne)

      val votesTwo = createVotes(Seq(No, No, NoAttend))
      val mpWithVoteTwo = MPWithVotes(2, "Teddy R", "Tories", votesTwo)

      val items = DataFactory.getItems(Seq(mpWithVotesOne, mpWithVoteTwo))

      val mockedDynamodbClient = mock[DynamodbClientTrait]
      val votesFetcher = new DynamodbVotesFetcher(mockedDynamodbClient)

      // when
      when(mockedDynamodbClient.scan(any())) thenReturn items
      val votesResult = votesFetcher.getVotes(2019)

      // then
      assert(votesResult.length == 2)
      assert(votesResult(0) == mpWithVotesOne)
      assert(votesResult(1) == mpWithVoteTwo)
    }
  }

}
