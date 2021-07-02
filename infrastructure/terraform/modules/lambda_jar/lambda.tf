resource "aws_lambda_function" "lambda" {
  function_name = var.function_name
  role          = aws_iam_role.lambda_main.arn
  filename      = var.file_name
  runtime = "java11"
  timeout       = 60
  memory_size = 1028
  reserved_concurrent_executions = 1
  tags = {
    Name    = var.tag_name
    Project = "vote-modes"
  }

  environment {
    variables = {
      QUEUE_URL = var.queue_url
    }
  }
  handler = var.handler_name
}