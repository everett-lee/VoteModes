package com.lee.aws

import awscala.Region
import awscala.dynamodbv2.{DynamoDB, Item, Table}
import com.amazonaws.services.dynamodbv2.model.Condition
import com.lee.model.MPWithVotes

class DynamodbClient(tableName: String) extends DynamodbClientTrait {
  private val defaultRegion: Region = Region.Ireland
  private implicit val dynamoDB: DynamoDB = DynamoDB.at(defaultRegion)
  var table: Option[Table] = Option.empty

  def setEndpoint(endpoint: String): Unit = {
    dynamoDB.setEndpoint(endpoint)
  }

  def scan(condition: Seq[(String, Condition)]): Seq[Item] = {
    if (table.isEmpty) {
      table = dynamoDB.table(tableName)
    }
    table.get.scan(condition)
  }

  def putItem(year: Int, id: Int, item: MPToVotesMap): Unit = {
    if (table.isEmpty) {
      table = dynamoDB.table(tableName)
    }
    table.get.putItem(year, id, item)
  }

  def deleteItem(year: Int, id: Int): Unit = {
    if (table.isEmpty) {
      table = dynamoDB.table(tableName)
    }
    table.get.deleteItem(year, id)
  }
}

// Create this class to match python DB input types. Only used for com.lee.integration tests.
case class MPToVotesMap(Name: String, Party: String, Votes: List[Map[String, String]])