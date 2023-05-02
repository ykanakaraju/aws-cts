import json
import datetime
import urllib
import boto3
import uuid

s3_client = boto3.client("s3")
dynamodb_client = boto3.resource('dynamodb')
table = dynamodb_client.Table('step_fn_demo_table')

def lambda_handler(message, context):

    bucket_name = message['sourceBucket']
    s3_file_name = message['objectKey']
    resp = s3_client.get_object(Bucket=bucket_name, Key=s3_file_name)
    data = resp['Body'].read().decode("utf-8")
    print(data)
    
    users = data.split("\n")
    row_count = 0
    
    for user in users:
        #print(user)        
        user_data = user.split(",")
        row_id = str(uuid.uuid1())	
        
        table.put_item(
            Item = {
                "row_id" : row_id,
                "id" : user_data[0],
                "name": user_data[1],
                "gender": user_data[2],
                "age": user_data[3],
                "mobile": user_data[4]
            }
        )        
        row_count += 1

    print( str(row_count) + " items inserted to DynamoDb table")
    print(message)

    response = {}
    response['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    response['message'] = str(row_count) + " items insert to DynamoDb table"

    return response