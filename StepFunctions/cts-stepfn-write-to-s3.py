import json
import datetime
import urllib
import boto3

s3_client = boto3.client('s3')

def lambda_handler(message, context):
    
    source_bucket = message['sourceBucket']
    object_key = message['objectKey']
    target_bucket = 'iquiz.stepfn.s3.output'
    copy_source = {'Bucket': source_bucket, 'Key': object_key}

    try:
        print ("Using waiter to waiting for object to persist through s3 service")
        waiter = s3_client.get_waiter('object_exists')
        waiter.wait(Bucket=source_bucket, Key=object_key)
        s3_client.copy_object(Bucket=target_bucket, Key=object_key, CopySource=copy_source)
        print ("S3 file copied")
        destination = "dynamodb"
    except Exception as err:
        print ("Error -" + str(err))
        destination = "error"        
            
    response = {}    
    response['sourceBucket'] = source_bucket
    response['objectKey'] = object_key
    response['destination'] = destination

    return response