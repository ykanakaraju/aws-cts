import datetime
import json
import random
import boto3
import time

STREAM_NAME = "my-input-stream"

def get_random_data():
    current_temperature = round(10 + random.random() * 170, 2)
    if current_temperature > 160:
        status = "ERROR"
    elif current_temperature > 140 or random.randrange(1, 100) > 80:
        status = random.choice(["WARNING","ERROR"])
    else:
        status = "OK"
    return {
        'sensor_id': random.randrange(1, 100),
        'current_temperature': current_temperature,
        'status': status,
        'event_time': datetime.datetime.now().isoformat()
    }


def send_data(stream_name, kinesis_client):
    i=0
    while True:
        i=int(i)+1
        data = get_random_data()
        partition_key = str(data["sensor_id"])
        print(data)
        time.sleep(1)

        response=kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(data),
            PartitionKey=partition_key)
            
        print("Total ingested:"+str(i) +",ReqID:"+ response['ResponseMetadata']['RequestId'] + ",HTTPStatusCode:"+ str(response['ResponseMetadata']['HTTPStatusCode']))


if __name__ == '__main__':
    kinesis_client = boto3.client('kinesis')
    send_data(STREAM_NAME, kinesis_client)


