import json
import time, urllib
import boto3
import uuid

client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    
    transactionId = str(uuid.uuid1())	
    sourceBucket = event['Records'][0]['s3']['bucket']['name']
    objectKey = event['Records'][0]['s3']['object']['key']
    
    if (sourceBucket == "iquiz.stepfn.s3.input") :
        destination = "s3"
    else :
        destination = "dynamodb"        
        
    print(transactionId, sourceBucket, objectKey, destination)
    
    input = {
        "sourceBucket": sourceBucket,
        "objectKey": objectKey,
        "destination": destination
    }
    
    response = client.start_execution(
		stateMachineArn='arn:aws:states:us-east-1:157549686651:stateMachine:S3AndDDBStateMachine',
		name=transactionId,
		input=json.dumps(input)	
	)
