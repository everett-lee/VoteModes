resource "aws_dynamodb_table" "dynamodb-table" {
  name           = var.table_name
  billing_mode     = "PAY_PER_REQUEST"
  hash_key       = "DivisionElectionYear"
  range_key      = "DivisionDate"

  attribute {
    name = var.attribute_name_one #"DivisionElectionYear"
    type = var.attribute_type_one #"N"
  }

  attribute {
    name = var.attribute_name_two # "DivisionDate"
    type = var.attribute_type_two #"S"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = false
  }

  tags = {
    Name    = var.tag_name #"divisions-table"
    Project = "vote-modes"
  }
}