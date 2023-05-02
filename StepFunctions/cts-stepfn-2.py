import json
import datetime
import urllib
import boto3


def lambda_handler(message, context):
    # TODO implement

    print("Received from step function")
    print(message)

    response = {}
    response['destination'] = message['destination']
    response['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    response['message'] = "Write to DynamoDB"


    return response