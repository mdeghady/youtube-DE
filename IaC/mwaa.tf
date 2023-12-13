##################################################################################
# Amazon Managed Workflows for Apache Airflow
##################################################################################

module "mwaa" {
  source = "aws-ia/mwaa/aws"

  name              = "youtube-de-mwaa"
  airflow_version   = "2.6.3"
  environment_class = "mw1.medium"

  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = [module.vpc.private_subnets[0], module.vpc.private_subnets[1]]

  min_workers           = 1
  max_workers           = 10
  webserver_access_mode = "PUBLIC_ONLY" # Default PRIVATE_ONLY for production environments


  create_iam_role = true
  iam_role_additional_policies = {
    #give mwaa full access to s3 and glue to make it easy to upload & download files from s3 buckets & to trigger glue crawler
    "additional-policy-1" = data.aws_iam_policy.glue_full_access_policy.arn #which has been created in glue.tf file
    "additional-policy-2" = data.aws_iam_policy.s3_full_access_policy.arn   #which has been created in glue.tf file
  }
  create_security_group = true

  create_s3_bucket = false
  #MWAA requires a bucket which is blocked for all public access and has versioning enabled
  source_bucket_arn    = aws_s3_bucket.mwaa_bucket.arn
  requirements_s3_path = "requirements.txt"
  dag_s3_path          = "dags"

  logging_configuration = {
    dag_processing_logs = {
      enabled   = true
      log_level = "INFO"
    }

    scheduler_logs = {
      enabled   = true
      log_level = "INFO"
    }

    task_logs = {
      enabled   = true
      log_level = "INFO"
    }

    webserver_logs = {
      enabled   = true
      log_level = "INFO"
    }

    worker_logs = {
      enabled   = true
      log_level = "INFO"
    }
  }

  airflow_configuration_options = {
    "core.load_default_connections" = "true"
    "core.load_examples"            = "false"
    "webserver.dag_default_view"    = "tree"
    "webserver.dag_orientation"     = "TB"
    "logging.logging_level"         = "INFO"
  }

  depends_on = [aws_s3_bucket.mwaa_bucket,
    aws_s3_object.upload_requirements_file,
  aws_s3_object.upload_dags_folder]
  
  tags = var.project_tags
}


