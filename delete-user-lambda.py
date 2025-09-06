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
			data = json.loads(body)
		else:
			data = event  # Assume non-proxy integration

		# Assuming '_id' is the primary key (partition key)
		# Adjust if there's a sort key or different primary key
		if '_id' not in data:
			raise ValueError("Missing '_id' in request body")

		key = {
			'_id': data['_id']
		}

		response = table.delete_item(Key=key)

		return {
			'statusCode': 200,
			'body': json.dumps('Item deleted successfully!')
		}
	except Exception as e:
		return {
			'statusCode': 400,
			'body': json.dumps(f'Invalid request: {str(e)}')
		}
