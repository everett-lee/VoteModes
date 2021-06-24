package dao

import awscala.Region
import awscala.dynamodbv2.{DynamoDB, Item, Table}
import com.amazonaws.services.dynamodbv2.model.Condition

class DynamodbClient extends DynamodbClientTrait {
  private val defaultRegion: Region = Region.Ireland
  private implicit val dynamoDB: DynamoDB = DynamoDB.at(defaultRegion)

  def scan(tableName: String, condition: Seq[(String, Condition)]): Seq[Item] = {
    val table: Table = dynamoDB.table(tableName).get
    table.scan(condition)
  }
}