resource "aws_s3_bucket" "s3_bucket" {
  bucket = var.bucket_name
  acl    = "private"

  tags = {
    Name    = var.tag_name
    Project = "vote-modes"
  }
}