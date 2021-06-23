package dao.kModes

import constants.VoteDecision.{Aye, No, NoAttend}
import kModes.CentroidsHelperMain
import model.{MPWithVotes, VotePair}
import org.scalatest.wordspec.AnyWordSpec

class CentroidsHelperMainTest extends AnyWordSpec {
  val centroidsHelper = new CentroidsHelperMain()

  val votesOne = List(VotePair(1, Aye), VotePair(2, No), VotePair(3, NoAttend), VotePair(4, Aye), VotePair(5, No))
  val votesTwo = List(VotePair(1, Aye), VotePair(2, NoAttend), VotePair(3, No), VotePair(4, NoAttend), VotePair(5, NoAttend))
  val votesThree = List(VotePair(1, No), VotePair(2, No), VotePair(3, Aye), VotePair(4, No), VotePair(5, No))
  val votesFour = List(VotePair(1, Aye), VotePair(2, Aye), VotePair(3, Aye), VotePair(4, NoAttend), VotePair(5, Aye))
  val votesFive = List(VotePair(1, NoAttend), VotePair(2, NoAttend), VotePair(3, No), VotePair(4, NoAttend), VotePair(5, NoAttend))
  val votesSix = List(VotePair(1, No), VotePair(2, No), VotePair(3, No), VotePair(4, Aye), VotePair(5, NoAttend))
  val votesSeven = List(VotePair(1, NoAttend), VotePair(2, Aye), VotePair(3, Aye), VotePair(4, Aye), VotePair(5, Aye))
  val votesEight = List(VotePair(1, No), VotePair(2, No), VotePair(3, No), VotePair(4, Aye), VotePair(5, NoAttend))

  val MPs = Vector(MPWithVotes(0, "Mark E Smith", "The Fall", votesOne),
    MPWithVotes(1, "Richard D James", "Aphex", votesTwo),
    MPWithVotes(2, "Mark K", "Sun Kil Moon", votesThree),
    MPWithVotes(3, "Mason Mount", "Chael Sea", votesFour),
    MPWithVotes(4, "A Allen", "Trimley", votesFive),
    MPWithVotes(5, "T Werner", "Just Wide", votesSix),
    MPWithVotes(6, "SP Morrissey", "Controversial", votesSeven),
    MPWithVotes(7, "The last one", "Has band", votesEight),
  )

  val centroidVotesOne = List(VotePair(1, No), VotePair(2, No), VotePair(3, NoAttend), VotePair(4, Aye), VotePair(5, Aye))
  val centroidVotesTwo = List(VotePair(1, Aye), VotePair(2, Aye), VotePair(3, Aye), VotePair(4, Aye), VotePair(5, Aye))
  val centroidVotesThree = List(VotePair(1, No), VotePair(2, NoAttend), VotePair(3, Aye), VotePair(4, No), VotePair(5, No))

  val centroids = Vector(MPWithVotes(-1, "Centroid 1", "One", centroidVotesOne),
    MPWithVotes(-2, "Centroid 2", "Two", centroidVotesTwo),
    MPWithVotes(-3, "Centroid 3", "Two", centroidVotesThree)
  )

  "The initCentroids method" should {
    // given
    "Initialise an array of K centroids" in {
      // when
      val centroids = centroidsHelper.initCentroids(MPs, 3)

      // then
      assert(centroids.size == 3)
      assert(centroids.to(Set).subsetOf(MPs.toSet))
    }

    "Throw when K > length" in {
      assertThrows[IllegalArgumentException] {
        centroidsHelper.initCentroids(MPs, MPs.size + 1)
      }
    }
  }

  "The calculateDistance method" should {
    // given
    val votesShort = List(VotePair(1, No))

    "Return no distance form itself" in {
      // when
      val distance = centroidsHelper.calculateDistance(votesOne, votesOne)

      // then
      assert(distance == 0)
    }

    "Return distance of four" in {
      // when
      val distance = centroidsHelper.calculateDistance(votesOne, votesTwo)

      // then
      assert(distance == 4)
    }

    "Return distance of five" in {
      // when
      val distance = centroidsHelper.calculateDistance(votesTwo, votesThree)

      // then
      assert(distance == 5)
    }

    "Return distance of two" in {
      // when
      val distance = centroidsHelper.calculateDistance(votesFour, votesSeven)

      // then
      assert(distance == 2)
    }

    "Throw when List sizes mismatched" in {
      assertThrows[IllegalArgumentException] {
        centroidsHelper.calculateDistance(votesOne, votesShort)
      }
    }
  }

  "The calculateClosestCentroid method" should {

    "Assign votesOne to CentroidOne" in {
      // when
      val centroid = centroidsHelper.calculateClosestCentroid(MPs(0), centroids)
      // then
      assert(centroid == -1)
    }

    "Assign votesTwo to centroidTwo or centroidThree" in {
      // when
      val centroid = centroidsHelper.calculateClosestCentroid(MPs(1), centroids)
      // then
      assert(centroid == -2 || centroid == -3)
    }

    "Assign votesThree to centroidThree" in {
      // when
      val centroid = centroidsHelper.calculateClosestCentroid(MPs(2), centroids)
      // then
      assert(centroid == -3)
    }

    "Assign votesFour to centroidTwo" in {
      // when
      val centroid = centroidsHelper.calculateClosestCentroid(MPs(3), centroids)
      // then
      assert(centroid == -2)
    }

    "Assign votesFive to centroidThree" in {
      // when
      val centroid = centroidsHelper.calculateClosestCentroid(MPs(4), centroids)
      // then
      assert(centroid == -3)
    }

    "Assign votesSix to centroidOne" in {
      // when
      val centroid = centroidsHelper.calculateClosestCentroid(MPs(5), centroids)
      // then
      assert(centroid == -1)
    }

    "Assign votesSeven to centroidTwo" in {
      // when
      val centroid = centroidsHelper.calculateClosestCentroid(MPs(6), centroids)
      // then
      assert(centroid == -2)
    }

    "Assign votesEight to centroidOne" in {
      // when
      val centroid = centroidsHelper.calculateClosestCentroid(MPs(7), centroids)
      // then
      assert(centroid == -1)
    }
  }

  "The groupByCentroids method" should {
    "Group the MPs correctly" in {
      // when
      val grouped = centroidsHelper.groupByCentroid(MPs, centroids)
      // then
      assert(grouped(-1) == Vector(MPs(0), MPs(5), MPs(7)))
      assert(grouped(-2) == Vector(MPs(1), MPs(3), MPs(6)))
      assert(grouped(-3) == Vector(MPs(2), MPs(4)))
    }
  }

  "Do shit" in {
    val a = List("B", "S", "T", "Y")
    val b = List("A", "B", "C", "D")
    val c = List("B", "Circle", "Triangle", "Rhombus")
    val d = List("A", "B", "C", "D")

    val in = List(a, b, c, d)
    val out = in.map(inList => inList.tail)
    val items = in.map(inList => inList.head)

    println(out)
    println(items)
    println(items.groupBy(identity).maxBy(_._2.size)._1)
  }
}
