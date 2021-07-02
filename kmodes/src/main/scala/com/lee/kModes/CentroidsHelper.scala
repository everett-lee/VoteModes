package com.lee.kModes

import com.lee.model.{MP, MPWithVotes, VotePair}

import scala.util.Random

trait CentroidsHelper[A <: Seq[MP], B <: Seq[VotePair]] {
  val randomGenerator: Random.type = scala.util.Random

  def initCentroids(MPsWithVotes: A, K: Int): A

  def calculateDistance(votes: B, centroid: B, acc: Int): Int

  def calculateClosestCentroid(MPWithVotes: MPWithVotes, centroids: A): Int

  def groupByCentroid(MPsWithVotes: A, centroids: A): Map[Int, A]

  def calculateCentroid(groupedMPs: A, centroidId: Int): MPWithVotes
}
