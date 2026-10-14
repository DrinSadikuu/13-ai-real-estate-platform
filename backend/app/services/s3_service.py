
import boto3

from app.core.config import get_settings


class S3Service:
    def __init__(self):
        settings = get_settings()

        self.bucket_name = settings.s3_bucket_name

        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )

    def upload_file(self, file_content: bytes, file_key: str):
        self.client.put_object(
            Bucket=self.bucket_name,
            Key=file_key,
            Body=file_content,
            ContentType="application/pdf",
        )

        return file_key
