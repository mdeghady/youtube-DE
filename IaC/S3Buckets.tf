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

#s3 bucket for cleaned parquet data
resource "aws_s3_bucket" "cleaned_data_bucket" {
  bucket        = "md-youtube-de-cleaned-data"
  force_destroy = true
  tags          = var.project_tags
}

##################################################################################
# MWAA S3 Bucket
##################################################################################

#MWAA requires a bucket which is blocked for all public access and has versioning enabled
resource "aws_s3_bucket" "mwaa_bucket" {
  #It's private by default
  bucket        = "md-mwaa"
  force_destroy = true
  tags          = var.project_tags
}

#add versioning to mwaa bucket
resource "aws_s3_bucket_versioning" "mwaa_bucket_versioning" {
  bucket = aws_s3_bucket.mwaa_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

#upload dags folder to MWAA bucket
resource "aws_s3_object" "upload_dags_folder" {
  for_each = fileset(var.mwaa_dags_folder, "**")
  bucket   = aws_s3_bucket.mwaa_bucket.id
  key      = "dags/${each.value}"
  source   = "${var.mwaa_dags_folder}${each.value}"

}

#upload mwaa requirements file to MWAA bucket
resource "aws_s3_object" "upload_requirements_file" {
  bucket = aws_s3_bucket.mwaa_bucket.id
  key    = "requirements.txt"
  source = var.mwaa_requirements_file

}



