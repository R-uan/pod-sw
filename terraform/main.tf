provider "google" {
  project     = "pod-sw"
  region      = "us-central1"
  credentials = file("credentials/terraform-key.json")
}

provider "google-beta" {
  project     = "pod-sw"
  region      = "us-central1"
  credentials = file("credentials/terraform-key.json")
}

data "archive_file" "function_zip" {
  type        = "zip"
  source_dir  = "../src/"
  output_path = "../function.zip"
}

// Cria um local de armazenamento para o código.
resource "google_storage_bucket" "function_bucket" {
  name                        = "star_wars_api_code"
  location                    = "US"
  uniform_bucket_level_access = true
}


// Pega o código armazenado.
resource "google_storage_bucket_object" "zip" {
  name   = "function.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = data.archive_file.function_zip.output_path
}

// Cria o "google function"
resource "google_cloudfunctions2_function" "star_wars_api" {
  name     = "star-wars-api-function"
  location = "us-central1"

  build_config {
    runtime     = "python312"
    entry_point = "star_wars_api"

    source {
      storage_source {
        bucket = google_storage_bucket.function_bucket.name
        object = google_storage_bucket_object.zip.name
      }
    }
  }

  service_config {
    available_cpu      = "1"
    available_memory   = "256Mi"
    timeout_seconds    = 60
    max_instance_count = 3
  }
}

// Openapi template
data "template_file" "openapi" {
  template = file("${path.module}/openapi.yaml.tpl")
  vars = {
    backend_url = google_cloudfunctions2_function.star_wars_api.service_config[0].uri
  }
}

resource "google_api_gateway_api" "api_gw" {
  provider = google-beta
  api_id   = "sw-api"
}

resource "google_api_gateway_api_config" "api_gw" {
  provider = google-beta
  api      = google_api_gateway_api.api_gw.api_id
  openapi_documents {
    document {
      path     = "openapi.yaml"
      contents = base64encode(data.template_file.openapi.rendered)
    }
  }
}
data "google_project" "project" {}

resource "google_cloud_run_service_iam_member" "allow_gateway" {
  provider = google-beta
  service  = google_cloudfunctions2_function.star_wars_api.service_config[0].service
  location = google_cloudfunctions2_function.star_wars_api.location
  role     = "roles/run.invoker"
  member   = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

resource "google_api_gateway_gateway" "gateway" {
  provider   = google-beta
  api_config = google_api_gateway_api_config.api_gw.id
  gateway_id = "sw-gateway"
}

