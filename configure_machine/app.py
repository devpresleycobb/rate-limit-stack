import os

def lambda_handler(event, context):
    request_id = context.aws_request_id
    batch_size = os.environ['BATCH_SIZE']
    bucket_name = os.environ['BUCKET_NAME']
    return {
        "request_id": request_id,
        "batch_size": batch_size,
        "bucket_name": bucket_name,
    }