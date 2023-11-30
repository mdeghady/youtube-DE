##################################################################################
# VPC DATA
##################################################################################

data "aws_availability_zones" "azs" {}

##################################################################################
# VPC MODULE
##################################################################################

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "youtube-DE-vpc"
  cidr = var.vpc_cidr

  azs             = slice(data.aws_availability_zones.azs.names,0,2)
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets

  
  

  tags = {
    Terraform = "true"
    Environment = "dev"
    project = "youtube-DE"
  }
}