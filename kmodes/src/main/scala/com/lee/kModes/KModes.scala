package com.lee.kModes

import com.lee.model.MP

trait KModes[A <: Seq[MP], B <: Seq[MP]] {
  def compute(MPsWithVotes: A): Map[Int, B]
}
