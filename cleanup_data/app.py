import boto3

def lambda_handler(event, context):
    request_id = event['config'].get('request_id')
    bucket_name = event['config'].get('bucket_name')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.objects.filter(Prefix=request_id).delete()