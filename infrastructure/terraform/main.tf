provider "aws" {
  region = "eu-west-3"
}

# IAM Role for EC2 to access S3
resource "aws_iam_role" "ec2_s3_access" {
  name = "ec2-s3-access-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy to grant full S3 access
resource "aws_iam_policy" "s3_full_access" {
  name        = "ec2-s3-full-access-policy"
  description = "Allow EC2 to manage S3 buckets"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = "s3:*",
        Effect   = "Allow",
        Resource = "*"
      }
    ]
  })
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "attach_s3_policy" {
  role       = aws_iam_role.ec2_s3_access.name
  policy_arn = aws_iam_policy.s3_full_access.arn
}

# Create an instance profile for the EC2 IAM Role
resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "ec2-s3-instance-profile"
  role = aws_iam_role.ec2_s3_access.name
}

# Attach instance profile to the existing EC2 instance
resource "aws_instance_profile_attachment" "attach_instance_profile" {
  instance_id         = "i-06f7d3dc2653df003"
  iam_instance_profile = aws_iam_instance_profile.ec2_instance_profile.name
}

# S3 Bucket: Stock Price ETL
resource "aws_s3_bucket" "stock_price_etl_bucket" {
  bucket = "stock-price-etl-bucket"
  acl    = "private"
}

# Folders within the S3 bucket
resource "aws_s3_bucket_object" "raw_data_folder" {
  bucket = aws_s3_bucket.stock_price_etl_bucket.bucket
  key    = "raw-data/"
}

resource "aws_s3_bucket_object" "transformed_data_folder" {
  bucket = aws_s3_bucket.stock_price_etl_bucket.bucket
  key    = "transformed-data/"
}

output "bucket_name" {
  value = aws_s3_bucket.stock_price_etl_bucket.bucket
}





# provider "aws" {
#   region = "eu-west-3"
# }

# resource "aws_s3_bucket" "stock-price-etl-bucket" {
#   bucket = "stock-price-etl-bucket"
#   acl    = "private"
# }

# # Folders within the main bucket
# resource "aws_s3_bucket_object" "raw-data" {
#   bucket = aws_s3_bucket.stock-price-etl-bucket.bucket
#   key    = "raw-data/"
# }

# resource "aws_s3_bucket_object" "transformed-data" {
#   bucket = aws_s3_bucket.stock-price-etl-bucket.bucket
#   key    = "transformed-data/"
# }

# output "bucket_name" {
#   value = aws_s3_bucket.stock-price-etl-bucket.bucket
# }



# # Provider configuration
# provider "aws" {
#   region = "eu-west-3"
# }

# # S3 Bucket and Subfolders
# resource "aws_s3_bucket" "stock_price_etl_bucket" {
#   bucket = "stock-price-etl-bucket"
#   acl    = "private"
# }

# resource "aws_s3_bucket_object" "raw_data" {
#   bucket = aws_s3_bucket.stock_price_etl_bucket.bucket
#   key    = "raw-data/"
# }

# resource "aws_s3_bucket_object" "transformed_data" {
#   bucket = aws_s3_bucket.stock_price_etl_bucket.bucket
#   key    = "transformed-data/"
# }

# output "bucket_name" {
#   value = aws_s3_bucket.stock_price_etl_bucket.bucket
# }

# # IAM Role for EC2
# resource "aws_iam_role" "ec2_s3_access_role" {
#   name = "ec2_s3_access_role"

#   assume_role_policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Effect = "Allow",
#         Action = "sts:AssumeRole",
#         Principal = {
#           Service = "ec2.amazonaws.com"
#         }
#       }
#     ]
#   })
# }

# # IAM Policy for S3 Access
# resource "aws_iam_policy" "s3_access_policy" {
#   name        = "S3AccessPolicy"
#   description = "Policy to allow EC2 to manage S3 buckets"

#   policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Effect = "Allow",
#         Action = [
#           "s3:CreateBucket",
#           "s3:PutObject",
#           "s3:GetObject",
#           "s3:ListBucket"
#         ],
#         Resource = [
#           "arn:aws:s3:::stock-price-etl-bucket",
#           "arn:aws:s3:::stock-price-etl-bucket/*"
#         ]
#       }
#     ]
#   })
# }

# # Attach Policy to the Role
# resource "aws_iam_role_policy_attachment" "attach_policy" {
#   role       = aws_iam_role.ec2_s3_access_role.name
#   policy_arn = aws_iam_policy.s3_access_policy.arn
# }

# # Instance Profile for EC2
# resource "aws_iam_instance_profile" "ec2_instance_profile" {
#   name = "ec2_s3_access_instance_profile"
#   role = aws_iam_role.ec2_s3_access_role.name
# }

# # EC2 Instance
# resource "aws_instance" "ec2_instance" {
#   ami           = "ami-0c55b159cbfafe1f0" # Replace with your AMI ID
#   instance_type = "t2.micro"
#   iam_instance_profile = aws_iam_instance_profile.ec2_instance_profile.name
#   key_name      = "your-key-pair" # Replace with your key pair

#   tags = {
#     Name = "S3-Access-Instance"
#   }
# }
