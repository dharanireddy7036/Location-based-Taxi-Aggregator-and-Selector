import pymongo
import json
from bson import json_util

mongo_client = pymongo.MongoClient(
    'mongodb+srv://team_raghav:mZaCudg6dUgfHjjU@taxi-cluster.i5ffecg.mongodb.net/?retryWrites=true&w=majority')

db = mongo_client['super_taxi']
collection = db["users"]


def lambda_handler(event, context):
    try:
        data = json.loads(json.dumps(event))
        body = json.loads(data.get('body'))

        phone_number = body["phone_number"]
        password = body["password"]

        check_user_exist = collection.find_one({"phone_number": phone_number})

        if check_user_exist == None:
            return json.dumps({
                "statusCode": 404,
                "status": False,
                "message": "User not found."
            })
        elif check_user_exist and check_user_exist['password'] != password:
            return json.dumps({
                "statusCode": 409,
                "status": False,
                "message": "Your password is invalid."
            })
        else:
            return json_util.dumps({
                "statusCode": 200,
                "status": True,
                "message": "User logged in successfully.",
                "data": check_user_exist
            })
    except Exception as e:
        return json.dumps({
            'statusCode': 500,
            'status': False,
            'body': json.dumps({'error': str(e)})
        })
