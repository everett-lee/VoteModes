package com.lee.service

import com.lee.model.MPWithVotes

trait VotesFetcher {
  def getVotes(electionYear: Int): Seq[MPWithVotes]
}
