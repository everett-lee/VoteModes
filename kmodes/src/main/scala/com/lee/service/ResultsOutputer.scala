package com.lee.service

import com.lee.model.MPDetails
import org.json4s.JObject
import org.json4s.JsonDSL._
import org.json4s.jackson.JsonMethods.{compact, render}

class ResultsOutputer {

  private def getPartyStats(mpDetails: Vector[MPDetails]): Map[String, Int] = {
    val groupedByParty = mpDetails.groupBy(_.mpParty).mapValues(partyList => partyList.size)

    groupedByParty.map { case (partyName, size) =>
      (partyName -> size)
    }
  }

  private def mapMPDetailsToJson(mpDetails: Vector[MPDetails]): Vector[JObject] = {
    mpDetails.map { mp =>
      ("Name" -> mp.mpName) ~
        ("Party" -> mp.mpParty)
    }
  }

  def createOutput(mpDetailsMap: Map[Int, Vector[MPDetails]]): String = {

    val json =
      ("Clusters" ->
        mpDetailsMap.map { case (id, mps) =>
          (id.toString ->
            ("PartyCounts" -> getPartyStats(mps)) ~
              ("Mps" -> mapMPDetailsToJson(mps))
            )
        }
        )

    compact(render(json))
  }
}
