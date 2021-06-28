package integration

import awscala.dynamodbv2.{Item, cond}
import dao.{DynamodbClient, MPToVotesMap}
import kModes.KModesData
import org.scalatest.wordspec.AnyWordSpec
import service.DynamodbVotesFetcher

class IntegrationTest extends AnyWordSpec {

  "The integration suite should" should {
    val dynamodbClient = new DynamodbClient("MPs")
    dynamodbClient.setEndpoint("http://localhost:4566")
    val votesFetcher = DynamodbVotesFetcher(dynamodbClient)

    // Create this class to match python DB input types
    val localMPs = KModesData.MPs.map(mp => {
      val votesAsMap = mp.votes.map(votePair => {
        Map("DivisionId" -> votePair.divisionId.toString,
          "Vote"-> votePair.voteDecision.toString)
      })
      MPToVotesMap(mp.mpName, mp.mpParty, votesAsMap)
    })

    "Give the correct output" in {
      localMPs.indices.foreach(index => {
        dynamodbClient.putItem(2019, index, localMPs(index))
      })

      val members: Seq[Item] = dynamodbClient.scan(Seq("MPElectionYear" -> cond.eq(2019)))
      val mpsWithVotes = votesFetcher.getVotes(2019)

      mpsWithVotes.foreach(mp => println(mp))

      localMPs.indices.foreach(index => {
        dynamodbClient.deleteItem(2019, index)
      })
    }
  }
}
