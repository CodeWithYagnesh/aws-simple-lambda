import json
import boto3
import base64

def lambda_handler(event, context):
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('users')

	try:
		if 'body' in event:
			body = event['body']
			if event.get('isBase64Encoded', False):
					body = base64.b64decode(body)
					body = body.decode('utf-8')
			item = json.loads(body)
		else:
			item = event  # Assume non-proxy integration where event is the parsed body

		# Validate that item is a dictionary
		if not isinstance(item, dict):
			raise ValueError("Item must be a dictionary")

		response = table.put_item(Item=item)

		return {
			'statusCode': 200,
			'body': json.dumps('Data inserted successfully!')
		}
	except Exception as e:
		return {
			'statusCode': 400,
			'body': json.dumps(f'Invalid request: {str(e)}')
		}
