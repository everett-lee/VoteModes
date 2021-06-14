resource "aws_lambda_function" "lambda" {
  function_name = var.function_name
  role          = aws_iam_role.lambda_main.arn
  package_type = "Image"
  image_uri = var.image_uri
  timeout       = 60
  memory_size = 1028
  reserved_concurrent_executions = 1
  tags = {
    Name    = var.tag_name
    Project = "vote-modes"
  }

  environment {
    variables = {
      QUEUE_URL = aws_sqs_queue.lambda_queue.id
    }
  }
}