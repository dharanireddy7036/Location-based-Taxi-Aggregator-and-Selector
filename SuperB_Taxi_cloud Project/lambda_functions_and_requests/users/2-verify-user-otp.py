import pymongo
import json

mongo_client = pymongo.MongoClient(
    'mongodb+srv://team_raghav:mZaCudg6dUgfHjjU@taxi-cluster.i5ffecg.mongodb.net/?retryWrites=true&w=majority')

db = mongo_client['super_taxi']
collection = db["users"]


def lambda_handler(event, context):
    try:
        data = json.loads(json.dumps(event))
        body = json.loads(data.get('body'))

        phone_number = body["phone_number"]
        otp = body["otp"]

        check_user_exist = collection.find_one({"phone_number": phone_number})

        if check_user_exist == None:
            return json.dumps({
                "statusCode": 404,
                "status": False,
                "message": "User not found."
            })
        elif check_user_exist and "is_verified" in check_user_exist and check_user_exist["is_verified"] == True:
            return json.dumps({
                "statusCode": 204,
                "status": False,
                "message": "User already verified."
            })
        elif check_user_exist and check_user_exist['otp'] != otp:
            return json.dumps({
                "statusCode": 401,
                "status": False,
                "message": "Entered OTP does not match."
            })
        else:
            collection.update_one(
                {"phone_number": phone_number},
                {'$set': {'is_verified': True}}
            )
            return json.dumps({
                "statusCode": 200,
                "status": True,
                "message": "User verified successfully."
            })
    except Exception as e:
        return json.dumps({
            'statusCode': 500,
            'status': False,
            'body': json.dumps({'error': str(e)})
        })
