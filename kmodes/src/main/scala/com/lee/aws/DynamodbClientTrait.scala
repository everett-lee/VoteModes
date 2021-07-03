package com.lee.aws

import awscala.dynamodbv2.Item
import com.amazonaws.services.dynamodbv2.model.Condition

// Trait for mocking
trait DynamodbClientTrait {
  def scan(condition: Seq[(String, Condition)]): Seq[Item]
}
