import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
ses = boto3.client('ses', region_name='us-east-1')
sns = boto3.client('sns', region_name='us-east-1')

def lambda_handler(event, context):
    http_method = event.get('requestContext', {}).get('http', {}).get('method', '')
    path = event.get('rawPath', '').replace('/prod', '')
    
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
        'body': json.dumps(result['Items'], cls=DecimalEncoder)
    }

def get_appointments():
    table = dynamodb.Table('Appointments')
    result = table.scan()
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(result['Items'], cls=DecimalEncoder)
    }

SENDER_EMAIL = 'tamar2030ovad@gmail.com'

def send_confirmation_email(recipient_email, client_name, service_name, date, time):
    try:
        ses.send_email(
            Source=SENDER_EMAIL,
            Destination={'ToAddresses': [recipient_email]},
            Message={
                'Subject': {'Data': 'אישור תור - Salon Smart', 'Charset': 'UTF-8'},
                'Body': {
                    'Text': {
                        'Data': (
                            f'שלום {client_name},\n\n'
                            f'תורך נקבע בהצלחה!\n\n'
                            f'פרטי התור:\n'
                            f'שירות: {service_name}\n'
                            f'תאריך: {date}\n'
                            f'שעה: {time}\n\n'
                            f'תודה שבחרת ב-Salon Smart!'
                        ),
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
    except Exception as e:
        print(f'SES send failed for {recipient_email}: {str(e)}')

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

    if body.get('email'):
        send_confirmation_email(
            recipient_email=body.get('email'),
            client_name=body.get('client_name', ''),
            service_name=body.get('service_name', ''),
            date=body.get('date', ''),
            time=body.get('time', '')
        )

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