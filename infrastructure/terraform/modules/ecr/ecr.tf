resource "aws_ecr_repository" "repo" {
  name                 = var.repo_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }

  tags = {
    Name    = var.tag_name
    Project = "vote-modes"
  }
}