import pymongo
import json
import boto3
import random
import hashlib
import base64
import uuid


def password_generator():
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"
    symbols = "@#$&_-()=%*:/!?+."
    string = lower + upper + numbers + symbols
    length = 8
    password = "".join(random.sample(string, length))
    return password


AWS_REGION = 'us-east-1'
sns_client = boto3.client('sns', aws_access_key_id="AKIAVKYQB4TVCRDCQLKY",
                          aws_secret_access_key="sYwcnYhenVyj7vq2YebuWtDvDtM9Suw7jS0PJDSa", region_name=AWS_REGION)

mongo_client = pymongo.MongoClient(
    'mongodb+srv://team_raghav:mZaCudg6dUgfHjjU@taxi-cluster.i5ffecg.mongodb.net/?retryWrites=true&w=majority')

db = mongo_client['super_taxi']
collection = db["drivers"]


def lambda_handler(event, context):
    try:
        data = json.loads(json.dumps(event))
        body = json.loads(data.get('body'))

        full_name = body["full_name"]
        email = body["email"]
        phone_number = body["phone_number"]
        vehicle_number = body["vehicle_number"]
        driving_license_no = body["driving_license_no"]
        vehicle_type = body["vehicle_type"]
        initial_location = body["initial_location"]
        current_location = body["current_location"]

        check_driver_exists = collection.find_one(
            {"vehicle_number": vehicle_number})

        if check_driver_exists != None:
            return json.dumps({
                "statusCode": 409,
                "status": False,
                "message": "Cab with same number cannot be registered."
            })
        else:
            password = password_generator()
            salt = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8')
            t_sha = hashlib.sha512()
            t_sha.update((password + salt).encode('utf-8'))
            hashed_password = base64.urlsafe_b64encode(
                t_sha.digest()).decode('utf-8')

            sns_client.publish(
                PhoneNumber=phone_number,
                Message=f"Your password for operating Taxi is {password}",
            )

            response = sns_client.subscribe(
                TopicArn='arn:aws:sns:us-east-1:366716511466:Superb_taxi',
                Protocol='email',
                Endpoint=email,
                ReturnSubscriptionArn=True
            )

            collection.insert_one({
                "full_name": full_name,
                "email": email,
                "phone_number": phone_number,
                "vehicle_number": vehicle_number,
                "driving_license_no": driving_license_no,
                "vehicle_type": vehicle_type,
                "plain_password": password,
                "hash": hashed_password,
                "salt": salt,
                "subscription_arn": response['SubscriptionArn'],
                "initial_location": initial_location,
                "current_location": current_location
            })

            return json.dumps({
                'statusCode': 201,
                'status': True,
                'message': 'Driver details inserted successfully.'
            })
    except Exception as e:
        return json.dumps({
            'statusCode': 500,
            'status': False,
            'body': json.dumps({'error': str(e)})
        })
