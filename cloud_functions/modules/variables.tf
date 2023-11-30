variable "project" {
  type    = string
  default = ""
}
variable "region" {
  type    = string
  default = "us-central1"
}
variable "zone" {
  type    = string
  default = "us-central1-a"
}
variable "name" {
  type = string
  default = "stopvm-tf"
}
variable "cron_exp" {
  type = string
  default = "0/2 * * * *"
}
variable "cron_description" {
  type =  string
  default = "Run every day at 9PM PST"
}
variable "service_account_email" {
  type = string
  default = "pocgke@xxx.iam.gserviceaccount.com"
}
variable "runtime" {
  type = string
  default = "python39"
}
variable "available_memory_mb" {
  default = 256
}
variable "source_archive_bucket" {
  type = string
  default = "gcp-terraform"
}
variable "source_archive_object" {
  type = string
  default = "terraform/function-source.zip"
}
variable "entry_point" {
  type = string
  default = "stop_vm_instance"
}
variable "fun_description" {
  type =  string
  default = "Stopping the vms"
}
variable "time_zone" {
  type = string
  default = "PST"
}