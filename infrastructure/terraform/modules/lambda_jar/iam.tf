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
      "sqs:ReceiveMessage",
    ]
    resources = [
      var.queue_arn,
    ]
  }
}

resource "aws_iam_policy" "lambda_sqs" {
  name               = "${var.function_name}-sqs-role"
  tags = {
    Name    = var.tag_name
    Project = "vote-modes"
  }
  policy = data.aws_iam_policy_document.sqs_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_sqs_attachment" {
  role       = aws_iam_role.lambda_main.name
  policy_arn = aws_iam_policy.lambda_sqs.arn
}

data "aws_iam_policy_document" "dynamodb_policy" {
  statement {
    effect = "Allow"
    actions = [
     "dynamodb:BatchGetItem",
     "dynamodb:DescribeTable",
     "dynamodb:GetItem",
     "dynamodb:Query",
     "dynamodb:Scan"
    ]

    resources = [
       "*"
    ]
  }
}

resource "aws_iam_policy" "lambda_dynamodb" {
  name               = "${var.function_name}-dynamodb-role"
  tags = {
    Name    = var.tag_name
    Project = "vote-modes"
  }
  policy = data.aws_iam_policy_document.dynamodb_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb_attachment" {
  role       = aws_iam_role.lambda_main.name
  policy_arn = aws_iam_policy.lambda_dynamodb.arn
}

resource "aws_cloudwatch_log_group" "example" {
  name              = "/aws/lambda/${var.function_name}"
  retention_in_days = 14
}

data "aws_iam_policy_document" "cloudwatch_policy" {
  statement {
    effect = "Allow"
    actions = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
    ]

    resources = [
       "arn:aws:logs:*:*:*"
    ]
  }
}

resource "aws_iam_policy" "lambda_logging" {
  name = "${var.function_name}_lambda_logging"
  path = "/"
  description = "IAM policy for logging from a ${var.function_name} lambda"

  policy = data.aws_iam_policy_document.cloudwatch_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_main.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

data "aws_iam_policy_document" "s3_policy_doc" {
  statement {
    effect = "Allow"
    actions = [
        "s3:*"
    ]

    resources = [
       "*"
    ]
  }
}

resource "aws_iam_policy" "s3_policy" {
  name               = "${var.function_name}-s3-role"
  tags = {
    Name    = var.tag_name
    Project = "vote-modes"
  }
  policy = data.aws_iam_policy_document.s3_policy_doc.json
}

resource "aws_iam_role_policy_attachment" "s3_policy_attachment" {
  role       = aws_iam_role.lambda_main.name
  policy_arn = aws_iam_policy.s3_policy.arn
}