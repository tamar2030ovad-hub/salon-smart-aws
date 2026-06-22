# Salon Smart

A serverless appointment booking system for a nail salon, built on AWS cloud infrastructure. The system allows clients to book, view, and cancel appointments independently, while providing administrators with a secure management panel to oversee and manage the schedule.

## Architecture Overview

The application follows a fully serverless architecture on AWS:

```
Client → Amazon S3 (Static Website) → Amazon API Gateway → AWS Lambda → Amazon DynamoDB
                                                                       → Amazon SES (confirmation email)
Admin  → Amazon Cognito (Authentication) → API Gateway → Lambda → DynamoDB
Lambda → Amazon CloudWatch (logs and monitoring)
IAM    → Manages permissions for all services
```

## AWS Services

| Service | Role | Type |
|---|---|---|
| Amazon S3 | Static website hosting | Required |
| API Gateway | REST API exposure | Required |
| AWS Lambda | Business logic (Python 3.12) | Required |
| Amazon DynamoDB | Database (Appointments, Clients, Services) | Required |
| AWS IAM | Permissions management | Required |
| Amazon Cognito | Admin authentication | Optional |
| Amazon SES | Confirmation emails | Optional |
| Amazon CloudWatch | Monitoring and logs | Optional |

## File Structure

```
salon-smart/
├── index.html              - Frontend website
├── lambda_function.py      - Lambda function code
├── lambda.zip              - Deployment package
└── architecture.svg        - AWS architecture diagram
```

## Installation

### Prerequisites

- An active AWS account
- AWS CLI installed and configured (`aws configure`)
- Git installed

### Step 1 — Create DynamoDB Tables

```bash
aws dynamodb create-table \
  --table-name Appointments \
  --attribute-definitions AttributeName=appointment_id,AttributeType=S \
  --key-schema AttributeName=appointment_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1

aws dynamodb create-table \
  --table-name Services \
  --attribute-definitions AttributeName=service_id,AttributeType=S \
  --key-schema AttributeName=service_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1

aws dynamodb create-table \
  --table-name Clients \
  --attribute-definitions AttributeName=client_phone,AttributeType=S \
  --key-schema AttributeName=client_phone,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

### Step 2 — Deploy the Lambda Function

```bash
aws lambda create-function \
  --function-name salon-smart-api \
  --runtime python3.12 \
  --role arn:aws:iam::417441750937:role/salon-smart-lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda.zip \
  --region us-east-1
```

### Step 3 — Create the API Gateway

```bash
aws apigatewayv2 create-api \
  --name salon-smart-api \
  --protocol-type HTTP \
  --region us-east-1
```

### Step 4 — Upload the Website to S3

```bash
aws s3 cp index.html s3://salon-smart-website-417441750937/ --region us-east-1
```

## Live Website

[http://salon-smart-website-417441750937.s3-website-us-east-1.amazonaws.com](http://salon-smart-website-417441750937.s3-website-us-east-1.amazonaws.com)

## Use Cases

1. A client books an appointment — selects a service, date, and time, and receives a confirmation email via SES.
2. A client cancels an appointment — cancels independently through the website; the system updates DynamoDB and sends a confirmation.
3. A client views available services — retrieves the full list of services, including prices and durations, from DynamoDB.
4. A client views their existing appointment — queries the system for current booking details.
5. An administrator logs in to the management panel — authenticates via Amazon Cognito and accesses the protected admin interface on the S3 website.
6. An administrator views and filters appointments — browses all scheduled appointments and filters by date or status.
7. An administrator cancels an appointment — removes a booking from the system via the management panel, authorized through the Cognito JWT token.

## Project Details

| Field | Value |
|---|---|
| Course | Cloud Systems Management (AWS) |
| Lecturer | Uri Berman |
| Institution | Azrieli College of Engineering, Jerusalem |
| Year | 2026 |
| Developers | Tamar | Eden | Nissa | Meytar |
