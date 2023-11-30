resource "google_cloud_scheduler_job" "stopvm-tf" {
  name        = var.name
  project     = var.project
  region      = var.region
  description = var.cron_description
  schedule    = var.cron_exp
  time_zone = var.time_zone
  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions_function.stopvm-tf.https_trigger_url
    oidc_token {
      service_account_email = var.service_account_email
    }
  }
}
