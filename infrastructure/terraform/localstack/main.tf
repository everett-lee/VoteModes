terraform {
  backend "local" {}
}

provider "aws" {
  access_key                  = "mock_access_key"
  region                      = "eu-west-1"
  secret_key                  = "mock_secret_key"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    lambda = "http://0.0.0.0:4574"
    iam    = "http://0.0.0.0:4593"
    dynamodb       = "http://localhost:4566"
  }
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
