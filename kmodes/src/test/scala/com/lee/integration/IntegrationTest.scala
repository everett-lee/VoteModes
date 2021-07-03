package com.lee.integration

import awscala.s3.{Bucket, PutObjectResult}
import com.amazonaws.services.s3.model.ObjectMetadata
import com.lee.aws.{DynamodbClient, MPToVotesMap, S3Client}
import com.lee.integration.IntegrationTest._
import com.lee.kModes.{KModesData, KModesMain}
import com.lee.service.{DynamodbVotesFetcher, ResultsOutputer}
import org.scalatest.BeforeAndAfterAll
import org.scalatest.wordspec.AnyWordSpec

class IntegrationTest extends AnyWordSpec with BeforeAndAfterAll {
  var bucket: Option[Bucket] = Option.empty

  override def beforeAll() = {
    bucket = Option(createBucket("test-bucket"))
  }
  override def afterAll() = {
    deleteS3Item("test-bucket", "01-01-20")
    deleteBucket("test-bucket")
  }

  "The com.lee.integration suite should" should {
    val votesFetcher = DynamodbVotesFetcher(com.lee.integration.IntegrationTest.dynamodbClient)
    val KModes = KModesMain()
    val outputer = new ResultsOutputer()

    // Create this to match python DB input types
    val localMPs = KModesData.MPs.map(mp => {
      val votesAsMap = mp.votes.map(votePair => {
        Map("DivisionId" -> votePair.divisionId.toString,
          "Vote"-> votePair.voteDecision.toString)
      })
      MPToVotesMap(mp.mpName, mp.mpParty, votesAsMap)
    })

    "Give the correct output" in {
      putDynamodbItems(localMPs)

      val mpsWithVotes = votesFetcher.getVotes(2019)
      val res = KModes.compute(mpsWithVotes.toVector)

      assert(res.size <= KModes.K)
      assert(res.values.flatten.toList.size == localMPs.size)

      val outJson = outputer.createOutput(res)
      val putResult = putS3Object(bucket.get, "01-01-20", outJson)

      assert(putResult.key == "01-01-20")

      val storedString = getS3Item("test-bucket", "01-01-20")
      assert(storedString == outJson)

      deleteDynamodbItems(localMPs)
    }
  }
}

object IntegrationTest {
  val s3Client = new S3Client()
  val dynamodbClient = new DynamodbClient("MPs")
  s3Client.setEndpoint("http://localhost:4566")
  dynamodbClient.setEndpoint("http://localhost:4566")

  def createBucket(name: String): Bucket = {
    s3Client.s3.createBucket(name)
  }

  def deleteBucket(name: String): Unit = {
    s3Client.s3.deleteBucket(name)
  }

  def putS3Object(bucket: Bucket, key: String, item: String): PutObjectResult = {
    val stream: java.io.InputStream = new java.io.ByteArrayInputStream(
      item.getBytes(java.nio.charset.StandardCharsets.UTF_8.name)
    )
    val metaData = new ObjectMetadata()
    metaData.setContentType("json")
    s3Client.s3.putObject(bucket, key, stream, metaData)
  }

  def getS3Item(bucketName: String, key: String): String = {
    val res = s3Client.s3.getObject(bucketName, key)
    val content = res.getObjectContent
    scala.io.Source.fromInputStream(content).mkString
  }

  def deleteS3Item(bucketName: String, name: String): Unit = {
    s3Client.s3.deleteObject(bucketName, name)
  }

  def putDynamodbItems(localMPs: Vector[MPToVotesMap]): Unit = {
    localMPs.indices.foreach(index => {
      dynamodbClient.putItem(2019, index, localMPs(index))
    })
  }

  def deleteDynamodbItems(localMPs: Vector[MPToVotesMap]): Unit = {
    localMPs.indices.foreach(index => {
      dynamodbClient.deleteItem(2019, index)
    })
  }
}