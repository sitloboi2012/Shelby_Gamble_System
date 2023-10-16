# -*- coding: utf-8 -*-
from pathlib import Path
import boto3
import os
from botocore.exceptions import ClientError
from constant import Constant

S3_CLIENT = boto3.client(
    "s3",
    aws_access_key_id=Constant.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Constant.AWS_SECRET_ACCESS_KEY,
)

S3_BUCKET = "shelby-raw-data-bucket"


def upload_file_object(file_name: Path, object_name: str) -> None:
    """
    Upload data as path to AWS S3 Bucket

    Args:
        file_name (Path): the path of the file
        object_name (str): the name of the file save onto data lake

    Raises:
        error: fail to upload file to AWS S3 Bucket due to ClientError
    """
    try:
        response = S3_CLIENT.upload_file(file_name, S3_BUCKET, object_name)
    except ClientError as error:
        raise error

    if response:
        print(f"Save {object_name} successfully to {S3_BUCKET}")


def upload_file_bytes(file_content: bytes, object_name: str) -> None:
    """
    Upload data as file content bytes to AWS S3 Bucket

    Args:
        file_content (bytes): the file content as bytes
        object_name (str): the name of the file save onto data lake

    Raises:
        error: fail to upload file to AWS S3 Bucket due to ClientError
    """
    try:
        response = S3_CLIENT.put_object(
            Body=file_content,
            Bucket=S3_BUCKET,
            Key=object_name,
        )
    except ClientError as error:
        raise error

    if response:
        print(f"Save {object_name} successfully to {S3_BUCKET}")


def download_file(object_name: str, save_path: str):
    return S3_CLIENT.download_file(S3_BUCKET, object_name, save_path)


def download_bucket(save_folder: str | Path):
    for object in S3_CLIENT.list_objects(Bucket=S3_BUCKET)["Contents"]:
        try:
            filename = object["Key"].rsplit("/", 1)[1]
        except IndexError:
            filename = object["Key"]

        local_filename = os.path.join(save_folder, filename)  # type: ignore
        download_file(filename, local_filename)
