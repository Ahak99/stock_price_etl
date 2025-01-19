resource "aws_s3_bucket" "stock-price-etl-bucket" {
  bucket = "stock-price-etl-bucket"
  acl    = "private"
}

# Folders within the main bucket
resource "aws_s3_bucket_object" "raw-data" {
  bucket = aws_s3_bucket.stock-price-etl-bucket.bucket
  key    = "raw-data/"
}

resource "aws_s3_bucket_object" "transformed-data" {
  bucket = aws_s3_bucket.stock-price-etl-bucket.bucket
  key    = "transformed-data/"
}

output "bucket_name" {
  value = aws_s3_bucket.stock-price-etl-bucket.bucket
}