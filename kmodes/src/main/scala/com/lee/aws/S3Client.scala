package com.lee.aws

import awscala.Region
import awscala.s3.{Bucket, PutObjectResult, S3}
import com.amazonaws.services.s3.model.ObjectMetadata

class S3Client {
  private val defaultRegion: Region = Region.Ireland
  val s3: S3 = S3.at(defaultRegion)

  def setEndpoint(endpoint: String): Unit = {
    s3.setEndpoint(endpoint)
  }

  def putS3Object(bucket: Bucket, key: String, item: String): PutObjectResult = {
    val stream: java.io.InputStream = new java.io.ByteArrayInputStream(
      item.getBytes(java.nio.charset.StandardCharsets.UTF_8.name)
    )
    val metaData = new ObjectMetadata()
    metaData.setContentType("json")
    s3.putObject(bucket, key, stream, metaData)
  }

  def getBucket(bucketName: String): Bucket = {
    val bucket = s3.bucket(bucketName)
    if (bucket.isEmpty) {
      throw new RuntimeException("No bucket with provided name")
    }
    bucket.get
  }

}
