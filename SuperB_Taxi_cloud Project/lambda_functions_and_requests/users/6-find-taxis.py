from pymongo import MongoClient, GEOSPHERE
import json
from bson.son import SON
from bson import json_util

mongo_client = MongoClient(
    'mongodb+srv://team_raghav:mZaCudg6dUgfHjjU@taxi-cluster.i5ffecg.mongodb.net/?retryWrites=true&w=majority')

db = mongo_client['super_taxi']
drivers = db["drivers"]
users = db["users"]

drivers.create_index([('initial_location', GEOSPHERE)])
drivers.create_index([('current_location', GEOSPHERE)])


def lambda_handler(event, context):
    try:
        data = json.loads(json.dumps(event))
        body = json.loads(data.get('body'))

        phone_number = body["phone_number"]
        vehicle_type = body["vehicle_type"]

        user_data = users.find_one({"phone_number": phone_number})

        customer_location = user_data['location']

        nearest_query = {
            'vehicle_type': vehicle_type,
            'current_location': SON([
                ("$near", {
                    "$geometry": customer_location,
                    "$maxDistance": 3000  # 3 kilometer in meters
                })
            ])
        }

        nearest_taxi = list(drivers.find(nearest_query))

        return json_util.dumps({
            "statusCode": 200,
            "status": True,
            "message": "Taxis fetched successfully.",
            "data": nearest_taxi
        })
    except Exception as e:
        return json.dumps({
            'statusCode': 500,
            'status': False,
            'body': json.dumps({'error': str(e)})
        })
