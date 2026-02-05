provider "google" {
  project = "pod-sw"
  region  = "us-central1"
}

resource "google_storage_bucket" "code" {
  name     = "func-code-bucket-123"
  location = "US"
}

resource "google_storage_bucket_object" "zip" {
  name   = "function.zip"
  bucket = google_storage_bucket.code.name
  source = "function.zip"
}

resource "google_cloudfunctions2_function" "hello" {
  name     = "hello"
  location = "us-central1"

  build_config {
    runtime     = "python313"
    entry_point = "star_wars_api"

    source {
      storage_source {
        bucket = google_storage_bucket.code.name
        object = google_storage_bucket_object.zip.name
      }
    }
  }

  service_config {
    available_cpu      = 1
    available_memory   = "256Mi"
    timeout_seconds    = 60
    max_instance_count = 3
  }
}

