provider "google-beta" {
  region  = var.region
  zone    = var.zone
  project = var.project
}

terraform {
  required_version = "~> 1.0"
  backend "gcs" {
    bucket = "pgcp-terraform"
    prefix = "terraform/functions/stopvm"
  }
  required_providers {
    google = {
      source = "local/providers/google"
    }
    google-beta = {
      source  = "local/providers/google-beta"
      version = "4.73.1"
    }
    random = {
      source  = "local/providers/random"
      version = "3.5.1"
    }
  }
}
