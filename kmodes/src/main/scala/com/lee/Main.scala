package com.lee

import com.amazonaws.services.lambda.runtime.Context
import com.amazonaws.services.lambda.runtime.events.SQSEvent
import com.lee.aws.S3Client
import com.lee.constants.Constants
import com.lee.kModes.KModesMain
import com.lee.service.{DynamodbVotesFetcher, ResultsOutputer}
import com.typesafe.scalalogging.Logger

class Main {
  val logger: Logger = Logger(Constants.loggerName)
  val s3Client = new S3Client()
  val outputer = new ResultsOutputer()

  val electionYear: Int = sys.env("ELECTION_YEAR").toInt
  val bucketName: String = sys.env("BUCKET_NAME")

  def handler(event: SQSEvent, context: Context): String = {
    logger.info("Starting handler")
    val votesFetcher = DynamodbVotesFetcher()
    val kModes = KModesMain()

    val votes = votesFetcher.getVotes(electionYear)
    val res = kModes.compute(votes.toVector)

    val json = outputer.createOutput(res)
    val bucket = s3Client.getBucket(bucketName)
    s3Client.putS3Object(bucket, java.time.LocalDate.now.toString, json)
    return "Success!"
  }
}
