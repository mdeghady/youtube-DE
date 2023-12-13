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
  azs  = slice(data.aws_availability_zones.azs.names, 0, 2) #choose two azs to work with

  cidr            = var.vpc_cidr
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets

  enable_nat_gateway     = true #because mwaa needs nat gateway
  one_nat_gateway_per_az = true

  nat_gateway_tags = var.project_tags
  tags             = var.project_tags
}
