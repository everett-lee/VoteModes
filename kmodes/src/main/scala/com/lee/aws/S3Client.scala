package com.lee.aws

import awscala.Region
import awscala.s3.S3

class S3Client {
  private val defaultRegion: Region = Region.Ireland
  val s3: S3 = S3.at(defaultRegion)

  def setEndpoint(endpoint: String): Unit = {
    s3.setEndpoint(endpoint)
  }
}
