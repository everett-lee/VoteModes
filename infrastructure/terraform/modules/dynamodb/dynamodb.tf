resource "aws_dynamodb_table" "dynamodb-table" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = var.attribute_name_one
  range_key    = var.attribute_name_two

  attribute {
    name = var.attribute_name_one
    type = var.attribute_type_one
  }

  attribute {
    name = var.attribute_name_two
    type = var.attribute_type_two
  }

  tags = {
    Name    = var.tag_name
    Project = "vote-modes"
  }
}