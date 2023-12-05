import pymongo
import json
from bson import json_util

mongo_client = pymongo.MongoClient(
    'mongodb+srv://team_raghav:mZaCudg6dUgfHjjU@taxi-cluster.i5ffecg.mongodb.net/?retryWrites=true&w=majority')

db = mongo_client['super_taxi']
drivers = db["drivers"]
bookings = db["bookings"]


def lambda_handler(event, context):
    try:
        data = json.loads(json.dumps(event))
        body = json.loads(data.get('body'))

        email = body["email"]

        driver_data = drivers.find_one({"email": email})

        if (driver_data == None):
            return json.dumps({
                'statusCode': 404,
                'status': False,
                'message': 'Driver details not found.'
            })
        else:
            rides = bookings.find({"taxi_id": driver_data["_id"]})

            if not rides:
                return json.dumps({
                    'statusCode': 404,
                    'status': False,
                    'message': 'No rides found for the driver.'
                })
            else:
                return json_util.dumps({
                    'statusCode': 200,
                    'status': True,
                    'message': 'Bookings data fetched successfully.',
                    'data': list(rides)
                })

    except Exception as e:
        return json.dumps({
            'statusCode': 500,
            'status': False,
            'body': json.dumps({'error': str(e)})
        })
