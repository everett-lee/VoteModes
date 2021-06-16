package dao

import awscala.Region
import awscala.dynamodbv2.{DynamoDB, Item, Table}
import com.amazonaws.services.dynamodbv2.model.Condition

object DynamodbClient {
  val defaultRegion = Region.Ireland
  implicit val dynamoDB = DynamoDB.at(defaultRegion)

  def scan(tableName: String, condition: Seq[(String, Condition)]): Seq[Item] = {
    val table: Table = dynamoDB.table(tableName).get
    table.scan(condition)
  }
}