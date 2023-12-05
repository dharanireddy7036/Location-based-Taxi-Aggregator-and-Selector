import pymongo
import json
import hashlib
import base64
import uuid

mongo_client = pymongo.MongoClient(
    'mongodb+srv://team_raghav:mZaCudg6dUgfHjjU@taxi-cluster.i5ffecg.mongodb.net/?retryWrites=true&w=majority')

db = mongo_client['super_taxi']
collection = db["users"]


def lambda_handler(event, context):
    try:
        data = json.loads(json.dumps(event))
        body = json.loads(data.get('body'))

        phone_number = body["phone_number"]
        user_name = body["user_name"]
        email = body["email"]
        password = body["password"]

        check_user_exist = collection.find_one({"phone_number": phone_number})

        if check_user_exist == None:
            return json.dumps({
                "statusCode": 404,
                "status": False,
                "message": "User not found."
            })
        else:
            salt = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8')
            t_sha = hashlib.sha512()
            t_sha.update((password + salt).encode('utf-8'))
            hashed_password = base64.urlsafe_b64encode(
                t_sha.digest()).decode('utf-8')

            collection.update_one(
                {"phone_number": phone_number},
                {
                    '$set': {
                        "user_name": user_name,
                        "email": email,
                        "plain_password": password,
                        "hash": hashed_password,
                        "salt": salt,
                        "location": {
                            "type": "Point",
                            "coordinates": [28.66455, 77.21887]
                        }
                    }
                }
            )
            return json.dumps({
                "statusCode": 200,
                "status": True,
                "message": "User details updated successfully."
            })
    except Exception as e:
        return json.dumps({
            'statusCode': 500,
            'status': False,
            'body': json.dumps({'error': str(e)})
        })
