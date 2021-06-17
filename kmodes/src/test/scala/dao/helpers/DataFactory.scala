package dao.helpers

import awscala.dynamodbv2.{Attribute, AttributeValue, Item}
import model.MPWithVotes


object DataFactory {
  private def convertToAttributes(mpWithVotes: MPWithVotes): Seq[Attribute] = {

    val id = Attribute("MemberId", AttributeValue.apply(AttributeValue.toJavaValue(mpWithVotes.id)))
    val name = Attribute("Name", AttributeValue.apply(AttributeValue.toJavaValue(mpWithVotes.mpName)))
    val electionYear = Attribute("MPElectionYear", AttributeValue.apply(AttributeValue.toJavaValue(2019)))
    val votesToMap = mpWithVotes.votes.map(pair =>
      Map("Vote" -> pair.voteDecision.toString, "DivisionId" -> pair.divisionId.toString))
    val votes = Attribute("Votes", AttributeValue.apply(AttributeValue.toJavaValue(votesToMap)))

    Seq(id, name, electionYear, votes)
  }

  def getItems(attributes: Seq[MPWithVotes]): Seq[Item] = {
    for {
      attribute <- attributes
    } yield new Item(null, convertToAttributes(attribute))
  }
}
