##################################################################################
# S3 Buckets
##################################################################################


module "s3_bucket" {
  source = "terraform-aws-modules/s3-bucket/aws"

  bucket = "md-youtube-de-landing"
  acl    = "private"

  control_object_ownership = true
  object_ownership         = "ObjectWriter"

  tags = {
    Terraform = "true"
    Environment = "dev"
    project = "youtube-DE"
  }
}


