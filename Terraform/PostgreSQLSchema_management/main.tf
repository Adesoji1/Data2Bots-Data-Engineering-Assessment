terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
    atlas = {
      source  = "ariga/atlas"
      version = "0.3.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "random_password" "password" {
  length  = 16
  special = true
}

data "aws_caller_identity" "current" {}

# VPC and Networking
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.16.1"

  name                 = "atlas-rds-demo"
  cidr                 = "10.0.0.0/16"
  azs                  = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  public_subnets       = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
  enable_dns_hostnames = true
  enable_dns_support   = true
}

###############################################################################
# Supporting Resources
################################################################################




resource "aws_db_subnet_group" "atlas" {
  name       = "atlas-rds-demo"
  subnet_ids = module.vpc.public_subnets
}

resource "aws_security_group" "rds" {
  name   = "atlas-demo"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

###############################################################################
# Master DB
################################################################################

# RDS PostgreSQL Instance
resource "aws_db_instance" "atlas-demo" {
  identifier             = "atlas-demo"
  instance_class         = "db.t3.micro"
  allocated_storage      = 5
  engine                 = "postgres"
  engine_version         = "13"
  username               = "atlas"
  password               = random_password.password.result
  db_subnet_group_name   = aws_db_subnet_group.atlas.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  parameter_group_name   = "default.postgres13"
  publicly_accessible    = true
  skip_final_snapshot    = true
}


# Atlas Schema Management
locals {
  dev_db_url = "postgres://atlas:pass@localhost:5432/example"
}

data "atlas_schema" "hello" {
  dev_db_url = local.dev_db_url
  src        = file("schema.hcl")
}

resource "atlas_schema" "hello" {
  hcl        = data.atlas_schema.hello.hcl
  dev_db_url = local.dev_db_url
  url        = "postgres://${aws_db_instance.atlas-demo.username}:${urlencode(random_password.password.result)}@${aws_db_instance.atlas-demo.endpoint}/example"
}

# Other resources and configurations based on the provided schemas...
