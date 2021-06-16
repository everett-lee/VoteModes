package dao.helpers

import awscala.dynamodbv2.{Attribute, Item, Table}

case class votePair(divisionId: Int, Map[])
case class MPAttributes(id: Int, name: String, votes)

object DataFactory {
  def getItems(attributesMap: Map[String, Seq[Attribute]]): Unit = {

    for {
      (itemName, attributes) <- attributesMap
    } yield new Item(null, attributes)
  }
}
