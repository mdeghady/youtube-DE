##################################################################################
# S3 Buckets
##################################################################################

#s3 bucket for landing json data
resource "aws_s3_bucket" "landing_data_bucket" {
  bucket        = "md-youtube-de-landing"
  force_destroy = true

  tags = {
    Terraform   = "true"
    Environment = "dev"
    project     = "youtube-DE"
  }
}

#s3 bucket for landing paquet data
resource "aws_s3_bucket" "cleaned_data_bucket" {
  bucket        = "md-youtube-de-cleaned-data"
  force_destroy = true

  tags = {
    Terraform   = "true"
    Environment = "dev"
    project     = "youtube-DE"
  }
}



