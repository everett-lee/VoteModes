resource "aws_lambda_function" "counter" {
  function_name = "counter"
  filename      = "lambda.zip"
  role          = "fake_role"
  handler       = "main.handler"
  runtime       = "nodejs8.10"
  timeout       = 30
}