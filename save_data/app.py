import os
import boto3
import json

def lambda_handler(event, context):
    request_id = event['config'].get('request_id')
    files = get_file_names(bucket_name=os.environ['BUCKET_NAME'], directory_name=request_id)
    results = download_results(bucket_name=os.environ['BUCKET_NAME'], file_names=files)
    save(results)

def download_results(bucket_name: str, file_names: list):
    client = boto3.client('s3')
    files = []
    for key in file_names:
        response = client.get_object(
            Bucket=bucket_name,
            Key=key
        )
        data = response['Body'].read().decode('utf-8')
        files.append(json.loads(data))
    return files

def get_file_names(bucket_name: str, directory_name: str):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    return [file.key
            for file in bucket.objects.filter(Prefix=directory_name)
            if file.key != f'{directory_name}/{os.environ["REQUEST_FILE_NAME"]}']

def save(data):
    print('Saving data', data)