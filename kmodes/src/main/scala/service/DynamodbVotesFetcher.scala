package service

import awscala.dynamodbv2.cond
import dao.DynamodbClient
import model.MPWithVotes

class DynamodbVotesFetcher extends VotesFetcher {

  override def getVotes(electionYear: Int): Seq[MPWithVotes] = {
    val votes = DynamodbClient.scan("MPs", Seq("MPElectionYear" -> cond.eq(2019)))

    Seq()
  }
}
