package service

import model.MPWithVotes

trait VotesFetcher {
  def getVotes(electionYear: Int): Seq[MPWithVotes]
}
