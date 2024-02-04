#create s3 bucket
resource "aws_s3_bucket" "mybucketdevops" {
  bucket = var.bucketname
}

resource "aws_s3_bucket_ownership_controls" "First" {
  bucket = aws_s3_bucket.mybucketdevops.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "First" {
  bucket = aws_s3_bucket.mybucketdevops.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "First" {
  depends_on = [
    aws_s3_bucket_ownership_controls.First,
    aws_s3_bucket_public_access_block.First,
  ]

  bucket = aws_s3_bucket.mybucketdevops.id
  acl    = "public-read"
}

resource "aws_s3_object" "index" {
  bucket = aws_s3_bucket.mybucketdevops.id
  key = "index.html"
  source = "Netflix clone/index.html"
  acl = "public-read"
  content_type = "text/html"
}

resource "aws_s3_object" "error" {
  bucket = aws_s3_bucket.mybucketdevops.id

  key = "error.html"
  source = "Netflix clone/error.html"
  acl = "public-read"
  content_type = "text/html"
}

resource "aws_s3_object" "styles" {
  bucket = aws_s3_bucket.mybucketdevops.id

  key = "styles.css"
  source = "Netflix clone/styles.css"
  acl = "public-read"
}

resource "aws_s3_object" "JS" {
  bucket = aws_s3_bucket.mybucketdevops.id

  key = "index.js"
  source = "Netflix clone/index.js"
  acl = "public-read"
}


resource "aws_s3_bucket_website_configuration" "website" {
  bucket = aws_s3_bucket.mybucketdevops.id
  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }

  depends_on = [ aws_s3_bucket_acl.First ]
}