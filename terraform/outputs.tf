# outputs.tf

# URL da Cloud Function
output "function_url" {
  description = "URL pública da Cloud Function"
  value       = google_cloudfunctions2_function.star_wars_api.service_config[0].uri
}

# Nome da função
output "function_name" {
  description = "Nome da Cloud Function"
  value       = google_cloudfunctions2_function.star_wars_api.name
}

# Região
output "function_region" {
  description = "Região da Cloud Function"
  value       = google_cloudfunctions2_function.star_wars_api.location
}

# Nome do bucket
output "bucket_name" {
  description = "Nome do bucket de armazenamento"
  value       = google_storage_bucket.function_bucket.name
}

output "gateway_url" {
  value       = google_api_gateway_gateway.gateway.default_hostname
  description = "API Gateway URL"
}

