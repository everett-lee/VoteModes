package com.lee.service

import awscala.dynamodbv2.{Item, cond}
import com.lee.constants.VoteDecision
import com.lee.aws.{DynamodbClient, DynamodbClientTrait}
import com.lee.model.{MPWithVotes, VotePair}
import com.lee.service.DynamodbVotesFetcher.attributesToMPWithVotes

import javax.management.InvalidAttributeValueException

class DynamodbVotesFetcher(dynamodbClient: DynamodbClientTrait) extends VotesFetcher {

  override def getVotes(electionYear: Int): Seq[MPWithVotes] = {
    val items = dynamodbClient.scan(Seq("MPElectionYear" -> cond.eq(electionYear)))

    items.map(item => attributesToMPWithVotes(item))
  }
}

object DynamodbVotesFetcher {
  def apply(dynamodbClient: DynamodbClientTrait = new DynamodbClient("MPs")): DynamodbVotesFetcher = {
    new DynamodbVotesFetcher(dynamodbClient)
  }

  def mapValuesToVotePair(inMap: Map[String, com.amazonaws.services.dynamodbv2.model.AttributeValue]): VotePair = {
    val divisionId = inMap("DivisionId").getS.toInt

    val vote = inMap("Vote").getS
    val decisionVote = vote match {
      case "Aye" => VoteDecision.Aye
      case "No" => VoteDecision.No
      case "NoAttend" => VoteDecision.NoAttend
      case _ => throw new InvalidAttributeValueException()
    }

    VotePair(divisionId, decisionVote)
  }

  def attributesToMPWithVotes(item: Item): MPWithVotes = {
    val attributes = item.attributes
    val id = attributes.filter(attribute => attribute.name == "MemberId")
      .head.value.n.getOrElse("-999").toInt

    val name = attributes.filter(attribute => attribute.name == "Name")
      .head.value.s.getOrElse("NoNameProvided")

    val party = attributes.filter(attribute => attribute.name == "Party")
      .head.value.s.getOrElse("NoPartyProvided")

    val votes = attributes.filter(attribute => attribute.name == "Votes")
      .head.value.l
      .map(value => Map("DivisionId" -> value.getM.get("DivisionId"), "Vote" -> value.getM.get("Vote")))
      .map(valueMap => mapValuesToVotePair(valueMap))
      .toList

    MPWithVotes(id, name, party, votes)
  }
}
