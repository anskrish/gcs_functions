resource "google_cloudfunctions_function" "stopvm-tf" {
  project               = var.project
  name                  = var.name
  description           = var.fun_description
  runtime               = var.runtime
  available_memory_mb   = var.available_memory_mb
  source_archive_bucket = var.source_archive_bucket
  source_archive_object = var.source_archive_object
  trigger_http          = true
  entry_point           = var.entry_point
  region                = var.region
  service_account_email = var.service_account_email
  environment_variables = {
    name = "terraform"
  }
}
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.stopvm-tf.project
  region         = google_cloudfunctions_function.stopvm-tf.region
  cloud_function = google_cloudfunctions_function.stopvm-tf.name

  role   = "roles/cloudfunctions.invoker"
  member = "serviceAccount:${var.service_account_email}"
}

