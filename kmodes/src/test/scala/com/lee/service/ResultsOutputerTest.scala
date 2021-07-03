package com.lee.service

import com.lee.model.MPDetails
import org.scalatest.wordspec.AnyWordSpec

class ResultsOutputerTest extends AnyWordSpec {
  val resultsOutputer = new ResultsOutputer()

  "A ResultsOutputer" should {
    "Create the correct json in" in {
      val expected = "{\"Clusters\":{\"1\":{\"PartyCounts\":{\"Engerland\":2,\"Big Face\":1},\"Mps\":[{\"Name\":\"Arry Kane\",\"Party\":\"Engerland\"},{\"Name\":\"Mase\",\"Party\":\"Engerland\"},{\"Name\":\"Richard D James\",\"Party\":\"Big Face\"}]},\"2\":{\"PartyCounts\":{\"Black Lodge\":2,\"Royale With Cheese\":1},\"Mps\":[{\"Name\":\"David Lynch\",\"Party\":\"Black Lodge\"},{\"Name\":\"Dale Cooper\",\"Party\":\"Black Lodge\"},{\"Name\":\"Travolta\",\"Party\":\"Royale With Cheese\"}]}}}"

      val detailsOne = MPDetails(1, "Arry Kane", "Engerland")
      val detailsTwo = MPDetails(2, "Mase", "Engerland")
      val detailsThree = MPDetails(3, "Richard D James", "Big Face")
      val detailsFour = MPDetails(4, "David Lynch", "Black Lodge")
      val detailsFive = MPDetails(5, "Dale Cooper", "Black Lodge")
      val detailsSix = MPDetails(6, "Travolta", "Royale With Cheese")

      val res = resultsOutputer
        .createOutput(Map(
          1 -> List(detailsOne, detailsTwo, detailsThree),
          2 -> List(detailsFour, detailsFive, detailsSix)
        ))

      assert(res == expected)
    }
  }

}
