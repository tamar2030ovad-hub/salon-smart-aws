import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
ses = boto3.client('ses', region_name='us-east-1')
sns = boto3.client('sns', region_name='us-east-1')

def lambda_handler(event, context):
    http_method = event.get('requestContext', {}).get('http', {}).get('method', '')
    path = event.get('rawPath', '')
    
    if path == '/services' and http_method == 'GET':
        return get_services()
    elif path == '/appointments' and http_method == 'POST':
        body = json.loads(event.get('body', '{}'))
        return create_appointment(body)
    elif path.startswith('/appointments/') and http_method == 'DELETE':
        appointment_id = path.split('/')[-1]
        return cancel_appointment(appointment_id)
    elif path == '/appointments' and http_method == 'GET':
        return get_appointments()
    else:
        return {'statusCode': 404, 'body': json.dumps({'message': 'Not found'})}

def get_services():
    table = dynamodb.Table('Services')
    result = table.scan()
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(result['Items'])
    }

def get_appointments():
    table = dynamodb.Table('Appointments')
    result = table.scan()
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(result['Items'])
    }

def create_appointment(body):
    table = dynamodb.Table('Appointments')
    clients_table = dynamodb.Table('Clients')
    
    appointment_id = str(uuid.uuid4())
    
    item = {
        'appointment_id': appointment_id,
        'client_name': body.get('client_name'),
        'client_phone': body.get('client_phone'),
        'email': body.get('email'),
        'service_name': body.get('service_name'),
        'date': body.get('date'),
        'time': body.get('time'),
        'status': 'active',
        'created_at': datetime.now().isoformat()
    }
    
    table.put_item(Item=item)
    
    clients_table.put_item(Item={
        'client_phone': body.get('client_phone'),
        'name': body.get('client_name'),
        'email': body.get('email')
    })
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'message': 'התור נקבע בהצלחה!', 'appointment_id': appointment_id})
    }

def cancel_appointment(appointment_id):
    table = dynamodb.Table('Appointments')
    
    table.update_item(
        Key={'appointment_id': appointment_id},
        UpdateExpression='SET #s = :s',
        ExpressionAttributeNames={'#s': 'status'},
        ExpressionAttributeValues={':s': 'cancelled'}
    )
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'message': 'התור בוטל בהצלחה!'})
    }