import pymongo
import json
import boto3
import random
import math


def generate_otp():
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    return random_str


AWS_REGION = 'us-east-1'
sns_client = boto3.client('sns',
                          aws_access_key_id="AKIAVKYQB4TVCRDCQLKY",
                          aws_secret_access_key="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",
                          region_name=AWS_REGION
                          )


mongo_client = pymongo.MongoClient(
    'mongodb+srv://team_raghav:mZaCudg6dUgfHjjU@taxi-cluster.i5ffecg.mongodb.net/?retryWrites=true&w=majority')

db = mongo_client['super_taxi']
collection = db["users"]


def lambda_handler(event, context):
    try:
        data = json.loads(json.dumps(event))
        body = json.loads(data.get('body'))

        phone_number = body["phone_number"]

        check_duplicate = collection.find_one({"phone_number": phone_number})

        if check_duplicate and check_duplicate['phone_number'] == phone_number:
            return json.dumps({
                "statusCode": 409,
                "status": False,
                "message": "Duplicate phone number found."
            })
        else:
            otp = generate_otp()

            sns_client.publish(
                PhoneNumber=phone_number,
                Message=f"Your OTP for Super Taxi is {otp}",
            )

            collection.insert_one({
                "phone_number": phone_number,
                "otp": otp
            })

            return json.dumps({
                'statusCode': 201,
                'status': True,
                'body': json.dumps({'message': 'OTP sent on your mobile.'})
            })

    except Exception as e:
        return json.dumps({
            'statusCode': 500,
            'status': False,
            'body': json.dumps({'error': str(e)})
        })
