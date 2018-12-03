import base64
import json
import boto3
import os

def lambda_handler(event, context):
	dynamodb = boto3.resource('dynamodb')
	# Parse the Arn value to extract table name
	table_split = os.environ['TABLE_NAME'].split(':', 5)
	table_name = table_split[5].replace("table/", "") 
	table = dynamodb.Table(table_name)
	for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
		payload = base64.b64decode(record["kinesis"]["data"])
		dictionary = json.loads(payload)
		with table.batch_writer() as batch:
			batch.put_item(
				Item={
					'id': dictionary['id'],
					'x': dictionary['x'],
					'y': dictionary['y'],
					'is_hot': dictionary['is_hot']
				}
			)
