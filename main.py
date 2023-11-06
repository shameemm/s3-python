import os
import boto3
# from botocore import NoCredentialsError
from PIL import Image

def compress_image(input_path, output_path):
    with Image.open(input_path) as img:
        img.save(output_path, quality=95, optimize=True)
        
def upload_to_s3(local_path, s3_bucket, s3_key):
    s3 = boto3.client('s3')
    print("++",s3)
    s3.upload_file(local_path, s3_bucket, s3_key)
    print(f'Uploaded {s3_key} to {s3_bucket}')
    os.remove(local_path)
    
def traverse_directory(directory_path, s3_bucket):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                input_path = os.path.join(root,file)
                output_path = f'temp_{file}'
                compress_image(input_path, output_path)
                s3_key = os.path.relpath(output_path,directory_path)
                upload_to_s3(output_path, s3_bucket, s3_key)
                
if __name__ == '__main__':
    aws_access_key = input('Enter AWS access key; ')
    aws_secret_key = input('Enter AWS secret key; ')
    s3_bucket = input('Enter target S3 bucket name: ')
    directory_path = input('Enter the directory path: ')
    
    boto3.setup_default_session(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    
    traverse_directory(directory_path,s3_bucket)