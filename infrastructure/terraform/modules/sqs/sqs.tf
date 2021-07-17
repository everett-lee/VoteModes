resource "aws_sqs_queue" "lambda_queue" {
  name                       = var.queue_name
  delay_seconds              = 10
  max_message_size           = 2048
  message_retention_seconds  = 86400
  visibility_timeout_seconds = 60

  tags = {
    Name    = var.tag_name
    Project = "vote-modes"
  }
}