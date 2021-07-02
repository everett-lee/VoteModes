package com.lee.model

sealed trait MP

case class MPDetails(id: Int, mpName: String, mpParty: String) extends MP

case class MPWithVotes(id: Int, mpName: String, mpParty: String, votes: List[VotePair]) extends MP