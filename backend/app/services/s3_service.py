
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
            endpoint_url=f"https://s3.{settings.aws_region}.amazonaws.com",
        )

    def upload_file(self, file_content: bytes, file_key: str):
        self.client.put_object(
            Bucket=self.bucket_name,
            Key=file_key,
            Body=file_content,
            ContentType="application/pdf",
        )

        return file_key

    def download_file(self, file_key: str) -> bytes:
        response = self.client.get_object(
            Bucket = self.bucket_name,
            Key = file_key,
        )
        return response["Body"].read()

    def generate_presigned_url(
            self,
            file_key: str,
            expiration: int = 300,
    ) -> str:
        url = self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": file_key,
            },
            ExpiresIn=expiration,
        )

        return url

    def delete_file(self, file_key: str) -> None:
        self.client.delete_object(
            Bucket=self.bucket_name,
            Key=file_key,
        )
