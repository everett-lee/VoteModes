package com.lee

import com.amazonaws.services.lambda.runtime.Context
import com.lee.constants.Constants
import com.lee.kModes.KModesMain
import com.lee.service.DynamodbVotesFetcher
import com.typesafe.scalalogging.Logger

class Main  {
  val logger = Logger(Constants.loggerName)

  def handler(event: String, context: Context): String = {

    logger.info("Starting handler")
    val votesFetcher = DynamodbVotesFetcher()
    val kModes = KModesMain()

    val votes = votesFetcher.getVotes(2019) // TODO: make env variable
    val res = kModes.compute(votes.toVector)

    res.foreach((a) => {
      logger.info("Key {}", a._1)
      logger.info("Val {}", a._2)
      logger.info(">>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<")
    })

    return "Success!"
  }
}
