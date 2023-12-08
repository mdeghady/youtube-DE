##################################################################################
# AWS GLUE CATALOG DATABASE
##################################################################################

resource "aws_glue_catalog_database" "glue_catalog_database" {
  name = "youtube-de-db"

  tags = {
    Terraform   = "true"
    Environment = "dev"
    project     = "youtube-DE"
  }
}

##################################################################################
# AWS GLUE CRAWLER ROLE POLICY
##################################################################################

resource "aws_iam_role" "glue_crawler_role" {
  name = "aws_glue_crawler_role"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "glue.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    Terraform   = "true"
    Environment = "dev"
    project     = "youtube-DE"
  }
}

data "aws_iam_policy" "glue_crawler_policy" {
  #Managed AWS policy for AWS GLUE
  arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

data "aws_iam_policy" "glue_s3_full_access_policy" {
  #Managed AWS policy for AWS GLUE to have full control to s3
  arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "glue_service_role_policy_attach" {
  #attach glue_crawler_policy to glue_crawler_role
  role       = aws_iam_role.glue_crawler_role.name
  policy_arn = data.aws_iam_policy.glue_crawler_policy.arn
}

resource "aws_iam_role_policy_attachment" "glue_s3_service_role_policy_attach" {
  #attach glue_crawler_policy to glue_crawler_role
  role       = aws_iam_role.glue_crawler_role.name
  policy_arn = data.aws_iam_policy.glue_s3_full_access_policy.arn
}

##################################################################################
# AWS GLUE CRAWLER
##################################################################################

resource "aws_glue_crawler" "glue-crawler" {
  database_name = aws_glue_catalog_database.glue_catalog_database.name
  name          = "youtube-de-crawler"
  role          = aws_iam_role.glue_crawler_role.arn
  #schedule      = "cron(0 1 * * *)" #run the crawler At 01:00 AM.

  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }

  s3_target {
    path = "s3://${aws_s3_bucket.cleaned_data_bucket.bucket}/raw_statistics/"
  }

  depends_on = [aws_s3_bucket.cleaned_data_bucket,
    aws_glue_catalog_database.glue_catalog_database,
  aws_iam_role.glue_crawler_role]

  tags = {
    Terraform   = "true"
    Environment = "dev"
    project     = "youtube-DE"
  }
}
