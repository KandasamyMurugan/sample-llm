output "main_bucket_id" {
  value = aws_s3_bucket.main.id
}

output "logging_bucket_id" {
  value = aws_s3_bucket.logging.id
}