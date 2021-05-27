resource "aws_lambda_function" "lambda" {
  function_name = var.function_name
  filename      = var.file_name
  role          = "fake_role"
  handler       = var.handler
  runtime       = "python3.8"
  timeout       = 60
  memory_size = 1028
  reserved_concurrent_executions = 1
  tags = {
    Name    = var.tag_name
    Project = "vote-modes"
  }
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_main" {
  name               = "${var.function_name}-assume-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
  tags = {
    Name    = var.tag_name
    Project = "vote-modes"
  }
}

data "aws_iam_policy_document" "sqs_policy" {
  statement {
    effect = "Allow"
    actions = [
      "sqs:SendMessage",
    ]
    resources = [
      aws_sqs_queue.lambda_queue.arn,
    ]
  }
}

resource "aws_iam_role" "lambda_sqs" {
  name               = "${var.function_name}-sqs-role"
  assume_role_policy = data.aws_iam_policy_document.sqs_policy.json
  tags = {
    Name    = var.tag_name
    Project = "vote-modes"
  }
}

data "aws_iam_policy_document" "dynamodb_policy" {
  statement {
    effect = "Allow"
    actions = [
     "dynamodb:BatchGetItem",
     "dynamodb:GetItem",
     "dynamodb:Query",
     "dynamodb:Scan",
     "dynamodb:BatchWriteItem",
     "dynamodb:PutItem",
     "dynamodb:UpdateItem"
    ]

    resources = [
       "*"
    ]
  }
}

resource "aws_iam_role" "lambda_dynamodb" {
  name               = "${var.function_name}-dynamodb-role"
  assume_role_policy = data.aws_iam_policy_document.dynamodb_policy.json
  tags = {
    Name    = var.tag_name
    Project = "vote-modes"
  }
}