resource "aws_lambda_function" "lambda" {
  function_name                  = var.function_name
  role                           = aws_iam_role.lambda_main.arn
  package_type                   = "Image"
  image_uri                      = var.image_uri
  timeout                        = 60
  memory_size                    = 1028
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
}

resource "aws_cloudwatch_event_rule" "cron_rule" {
    name = "lambda_cron_rule"
    description = "Fires fourth day each month"
    schedule_expression = "cron(0 1 3 * ? *)"
  tags = {
    Name    = var.tag_name
    Project = "vote-modes"
  }
}

resource "aws_lambda_permission" "cloudwatch_trigger_permission" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.lambda.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.cron_rule.arn
}

resource "aws_cloudwatch_event_target" "cron_target" {
  rule  = aws_cloudwatch_event_rule.cron_rule.name
  arn   = aws_lambda_function.lambda.arn
}