import com.amazonaws.services.lambda.runtime.Context
import kModes.KModesMain
import service.DynamodbVotesFetcher

class Main  {
  def handler(event: String, context: Context): String = {

    val votesFetcher = DynamodbVotesFetcher()
    val kModes = KModesMain()

    val votes = votesFetcher.getVotes(2019) // TODO: make env variable
    val res = kModes.compute(votes.toVector)

    res.foreach((a) => {
        println(f"Key ${a._1}")
        println(f"Val ${a._2}")
        println(">>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<")
    })

    return "Success!"
  }
}
