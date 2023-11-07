import os
import logging
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError
from PIL import Image

def compress_image(input_path, output_path):
    with Image.open(input_path) as img:
        img.save(output_path, quality=95, optimize=True)

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def traverse_directory(directory, s3_bucket):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                input_path = os.path.join(root, file)
                output_path = f'compressed_{file}'

                compress_image(input_path, output_path)
                upload_file(output_path, s3_bucket, os.path.relpath(output_path))

                # Clean up the compressed image
                os.remove(output_path)

if __name__ == '__main__':
    aws_access_key_id = input('Enter AWS Access Key ID: ')
    aws_secret_access_key = input('Enter AWS Secret Access Key: ')
    s3_bucket = input('Enter target AWS S3 bucket name: ')
    directory = input('Enter the directory path: ')

    os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
    os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key

    traverse_directory(directory, s3_bucket)