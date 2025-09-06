# Lambda Play: AWS Lambda + DynamoDB + API Gateway

NO MORE DISCUSSION.....

![image](/images/architecutre.png)


## 1. Create DynamoDB Table

1. Go to DynamoDB in AWS Console.
2. Click **Create Table**.
3. Set **Table name**: `users`
4. Set **Partition key**: `_id` (Type: String)
5. Click **Create table**.

## 2. Create Lambda Functions

### a. Create User Function

1. Go to Lambda in AWS Console.
2. Click **Create function**.
3. Set **Function name**: `create-user`
4. Choose **Runtime**: Python (any version)
5. Click **Create function**.
6. Write your code in `lambda_function.py` (or use `create-user-lambda.py`).
7. Click **Deploy**.
8. Click **Test** → create a test event → enter name → save.

**Error Handling:**
If you get an error about AWS roles:
- Go to **Configuration > Permissions > Execution role**.
- Click the role name (e.g., `create-user-role-*****`).
- Click **Add Permission > Attach Policies**.
- Attach `AmazonDynamoDBFullAccess`.

**Expected Error:**
If you see:
```json
{
	"statusCode": 400,
	"body": "\"Invalid request: An error occurred (ValidationException) when calling the PutItem operation: One or more parameter values were invalid: Missing the key _id in the item\""
}
```
This means you need to send data from the client via API Gateway.

---

### b. Get User Function

1. Repeat steps above, set **Function name**: `get-user`.
2. Use code from `get-user-lambda.py`.
3. Attach `AmazonDynamoDBReadOnlyAccess` to the role.

**Note:**
If you still get permission errors, wait a few minutes for the role to update.

---

### c. Delete User Function

1. Repeat steps above, set **Function name**: `delete-user`.
2. Use code from `delete-user-lambda.py`.
3. Attach `AmazonDynamoDBFullAccess` to the role.

**Expected Error:**
If you see:
```json
{
	"statusCode": 400,
	"body": "\"Invalid request: Missing '_id' in request body\""
}
```
You need to send data from the client via API Gateway.

---

## 3. Set Up API Gateway

1. Go to API Gateway in AWS Console.
2. Create a **REST API**.
3. Name your API.
4. Create resources and methods:
		- `/create` → POST → Lambda: `create-user`
		- `/get` → GET → Lambda: `get-user`
		- `/delete` → POST → Lambda: `delete-user`
5. Deploy the API:
		- Create a new stage (e.g., `v1`)
		- Click **Deploy**

**Invoke URL Example:**
```
https://<UNIQUE-ID>.execute-api.<REGION>.amazonaws.com/<STAGE>/<RESOURCE>
```

---

## 4. Test Your API

Use the invoke URL to call your endpoints and verify everything works!

### Example: Create User with cURL



```bash
curl -X POST \
	<YOUR_INVOKE_URL>/create \
	-H "Content-Type: application/json" \
	-d '{"_id": "user123", "name": "John Doe", "email": "john@example.com"}'
```

### Example: Get User with cURL
```bash
curl -X GET \
	<YOUR_INVOKE_URL>/get \
	-H "Content-Type: application/json"
```

### Example: delete User with cURL

```bash
curl -X POST \
	<YOUR_INVOKE_URL>/delete \
	-H "Content-Type: application/json" \
	-d '{"_id": "user123"}'
```


For More learn :

- https://catalog.workshops.aws/serverless-patterns/en-US/business-scenario
