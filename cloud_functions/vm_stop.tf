module "cloud_function" {
  source = "./modules"
  name = "stopvmtf"
  cron_exp = "0 9 * * *"
  runtime = "python39"
  source_archive_object = "terraform/function-source.zip"
  entry_point = "stop_vm_instance"
}
