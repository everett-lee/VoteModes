package model

import constants.VoteDecision.VoteDecision

case class VotePair(divisionId: Int, voteDecision: VoteDecision)
case class MPWithVotes(id: Int, mpName: String, mpParty: String, votes: Seq[VotePair])