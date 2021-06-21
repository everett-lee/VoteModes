package dao

import awscala.dynamodbv2.Item
import com.amazonaws.services.dynamodbv2.model.Condition

// Trait for mocking
trait DynamodbClientTrait {
  def scan(tableName: String, condition: Seq[(String, Condition)]): Seq[Item]
}