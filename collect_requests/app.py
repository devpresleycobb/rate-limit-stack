import boto3
import json

def lambda_handler(event, context):
    request_id = event['config'].get('request_id')
    bucket_name = event['config'].get('bucket_name')
    data = collect_requests()
    requests_key = save_to_s3(data=json.dumps(data),
               bucket_name=bucket_name,
               request_id=request_id,
               file_name='requests.json')
    return requests_key

def save_to_s3(data: bytes, bucket_name: str, request_id: str, file_name: str):
    key = f'{request_id}/{file_name}'
    s3 = boto3.resource('s3')
    object = s3.Object(bucket_name, key)
    object.put(Body=data)
    return key

def collect_requests():
    return  [{
                'id': '123',
                'report_date': '2021-08-02'
             },
             {
                'id': '456',
                'report_date': '2021-08-02'
             },
             {
                'id': '789',
                'report_date': '2021-08-02'
             }]