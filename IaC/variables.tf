variable "region" {
  type        = string
  description = "Region for AWS Resources"
  default     = "us-east-1"

}

variable "vpc_cidr" {
  type        = string
  description = "Vpc cidr block"
  default     = "10.0.0.0/16"

}

variable "public_subnets" {
  type        = list(string)
  description = "Vpc puplic subnets"
  default     = ["10.0.2.0/24", "10.0.4.0/24", "10.0.6.0/24", "10.0.20.0/24"]

}

variable "private_subnets" {
  type        = list(string)
  description = "Vpc private subnets"
  default     = ["10.0.12.0/24", "10.0.14.0/24", "10.0.16.0/24", "10.0.18.0/24"]

}

variable "mwaa_dags_folder" {
  type        = string
  description = "dags folder path"
  default     = "C:/Users/mosta/Desktop/youtube-DE/dags/"

}

variable "mwaa_requirements_file" {
  type        = string
  description = "requirement python libraries for mwaa"
  default     = "C:/Users/mosta/Desktop/youtube-DE/requirements.txt"
}

variable "project_tags" {
  type        = map(any)
  description = "key value pairs of the project_tags"
  default = {
    Terraform   = "true"
    Environment = "dev"
    project     = "youtube-DE"
  }
}
