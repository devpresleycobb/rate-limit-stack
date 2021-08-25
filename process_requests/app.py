import os
import boto3
import json

def lambda_handler(event, context):
    request_id = event['config'].get('request_id')
    requests_key = event.get('requests_key')
    chunk_id = context.aws_request_id
    if event.get('status'):
        chunk_keys = event.get('status').get('chunk_keys')
    else:
        chunk_keys = []
    unprocessed_requests = get_unprocessed_requests(bucket_name=os.environ['BUCKET_NAME'],
                                                    key=requests_key)
    remaining_requests = []
    if unprocessed_requests:
        remaining_requests, data = process_requests(unprocessed_requests=unprocessed_requests,
                                                    batch_size=int(os.environ['BATCH_SIZE']))
        chunk_key = save_chunk_to_s3(data=json.dumps(data),
                                     bucket_name=os.environ['BUCKET_NAME'],
                                     request_id=request_id,
                                     file_name=chunk_id)
        update_requests_file(data=json.dumps(remaining_requests),
                             bucket_name=os.environ['BUCKET_NAME'],
                             key=requests_key)
        chunk_keys.append(chunk_key)

    return {
        "loop": bool(len(remaining_requests)),
        "chunk_keys": chunk_keys
    }

def update_requests_file(data: bytes, bucket_name: str, key: str):
    s3 = boto3.resource('s3')
    object = s3.Object(bucket_name, key)
    object.put(Body=data)
    return key

def get_unprocessed_requests(bucket_name: str, key: str):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=key)
    data = response['Body'].read().decode('utf-8')
    return json.loads(data)

def save_chunk_to_s3(data: bytes, bucket_name: str, request_id: str, file_name: str):
    key = f'{request_id}/{file_name}'
    s3 = boto3.resource('s3')
    object = s3.Object(bucket_name, key)
    object.put(Body=data)
    return key

def process_requests(unprocessed_requests: list, batch_size: int):
    batch = unprocessed_requests[:batch_size]
    data = []
    for request in batch:
        print('request processed', request)
        data.append('mock response data data from api results')
    return [unprocessed_requests[batch_size:], data]