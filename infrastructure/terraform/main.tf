resource "aws_s3_bucket" "smap_data_bucket" {
  bucket = "smap-data-bucket"
  acl    = "private"
}

# Folders within the main bucket
resource "aws_s3_bucket_object" "raw_data_folder" {
  bucket = aws_s3_bucket.smap_data_bucket.bucket
  key    = "raw_data_bucket/"
}

resource "aws_s3_bucket_object" "transformed_data_folder" {
  bucket = aws_s3_bucket.smap_data_bucket.bucket
  key    = "transformed_data_bucket/"
}

output "bucket_name" {
  value = aws_s3_bucket.smap_data_bucket.bucket
}