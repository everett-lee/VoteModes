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

module "divisions_table" {
  source             = "../modules/dynamodb"
  table_name         = "Divisions"
  attribute_name_one = "DivisionElectionYear"
  attribute_type_one = "N"
  attribute_name_two = "DivisionDate"
  attribute_type_two = "S"
  tag_name           = "divisions-table"
}

module "mps_table" {
  source             = "../modules/dynamodb"
  table_name         = "MPs"
  attribute_name_one = "MPElectionYear"
  attribute_type_one = "N"
  attribute_name_two = "MemberId"
  attribute_type_two = "N"
  tag_name           = "mps-table"
}

module "lambda_repo" {
  source    = "../modules/ecr"
  repo_name = "lambda_downloader_repo"
  tag_name  = "lambda_downloader_repo"
}

module "sqs" {
  source     = "../modules/sqs"
  queue_name = "LambdaQueue"
  tag_name   = "downloader_lambda_app"
}

module "downloader_lambda" {
  source        = "../modules/lambda_image"
  function_name = "DownloaderLambda"
  tag_name      = "downloader_lambda_app"
  image_uri     = "540073770261.dkr.ecr.eu-west-1.amazonaws.com/lambda_downloader_repo:latest"
  queue_arn     = module.sqs.queue_arn
  queue_url     = module.sqs.queue_url
}

module "kmodes_lambda" {
  source        = "../modules/lambda_jar"
  function_name = "KModesLambda"
  tag_name      = "k_modes_lambda_app"
  file_name     = "votemodes.jar"
  handler_name  = "com.lee.Main::handler"
  queue_arn     = module.sqs.queue_arn
  queue_url     = module.sqs.queue_url
  bucket_name   = module.s3.bucket_id
  bucket_arn    = module.s3.bucket_arn
}

module "s3" {
  source      = "../modules/s3"
  tag_name    = "results_s3"
  bucket_name = "votemodes-results"
}