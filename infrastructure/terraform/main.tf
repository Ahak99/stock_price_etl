resource "aws_s3_bucket" "stock-price-etl-bucket" {
  bucket = "stock-price-etl-bucket"
  acl    = "private"
}

# Folders within the main bucket
resource "aws_s3_bucket_object" "raw_data" {
  bucket = aws_s3_bucket.stock-price-etl-bucket.bucket
  key    = "raw_data_bucket/"
}

resource "aws_s3_bucket_object" "transformed_data" {
  bucket = aws_s3_bucket.stock-price-etl-bucket.bucket
  key    = "transformed_data_bucket/"
}

output "bucket_name" {
  value = aws_s3_bucket.stock-price-etl-bucket.bucket
}