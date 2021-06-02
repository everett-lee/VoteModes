terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
}

module divisions_table {
  source = "../modules/dynamodb"
  table_name = "Divisions"
  attribute_name_one = "DivisionElectionYear"
  attribute_type_one = "N"
  attribute_name_two = "DivisionDate"
  attribute_type_two = "S"
  tag_name = "divisions-table"
}

module mps_table {
  source = "../modules/dynamodb"
  table_name = "MPs"
  attribute_name_one = "MPElectionYear"
  attribute_type_one = "N"
  attribute_name_two = "MemberId"
  attribute_type_two = "N"
  tag_name = "mps-table"
}

module lambda_repo {
  source = "../modules/ecr"
  repo_name = "lambda_downloader_repo"
  tag_name = "lambda_downloader_repo"
}

//
//module lambda {
//  source = "../modules/lambda"
//  function_name = "DownloaderLambda"
//  file_name = "downloader_lambda_app.zip"
//  handler = "downloader_lambda_app.lambda_handler"
//  tag_name = "downloader_lambda_app"
//  queue_name = "LambdaQueue"
//}