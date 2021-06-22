package dao.kModes

import constants.VoteDecision.{Aye, No, NoAttend}
import kModes.KModesMain
import model.{MPWithVotes, VotePair}
import org.scalatest.wordspec.AnyWordSpec


class KModesMainTest extends AnyWordSpec {
  val KModes = new KModesMain()

  "The initCentroids method" should {
    // given
    val MPs = Vector(MPWithVotes(0, "Mark E Smith", "The Fall", List()),
      MPWithVotes(1, "Richard D James", "Aphex", List()),
      MPWithVotes(2, "Mark K", "Sun Kil Moon", List()),
      MPWithVotes(3, "The last one", "Has band", List())
    )

    "Initialise an array of K centroids" in {
      // when
      val centroids = KModes.initCentroids(MPs, 3)

      // then
      assert(centroids.size == 3)
      assert(centroids.to(Set).subsetOf(MPs.toSet))
    }

    "Throw when K > length" in {
      assertThrows[IllegalArgumentException] {
        KModes.initCentroids(MPs, MPs.size + 1)
      }
    }
  }

  "The calculateDistance method" should {
    // given
    val votesOne = List(VotePair(1, Aye), VotePair(2, No), VotePair(3, NoAttend))
    val votesTwo = List(VotePair(1, No), VotePair(2, No), VotePair(3, No))
    val votesThree = List(VotePair(1, No), VotePair(2, No), VotePair(3, Aye))
    val votesFour = List(VotePair(1, No))

    "Return no distance form itself" in {
      // when
      val distance = KModes.calculateDistance(votesOne, votesOne)

      // then
      assert(distance == 0)
    }

    "Return distance of two" in {
      // when
      val distance = KModes.calculateDistance(votesOne, votesTwo)

      // then
      assert(distance == 2)
    }

    "Return distance of One" in {
      // when
      val distance = KModes.calculateDistance(votesTwo, votesThree)

      // then
      assert(distance == 1)
    }

    "Throw when List sizes mismatched" in {
      assertThrows[IllegalArgumentException] {
        KModes.calculateDistance(votesOne, votesFour)
      }
    }
  }
}
