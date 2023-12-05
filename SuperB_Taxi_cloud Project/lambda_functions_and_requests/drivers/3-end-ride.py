import pymongo
import json
from bson import json_util, ObjectId
import datetime

mongo_client = pymongo.MongoClient(
    'mongodb+srv://team_raghav:mZaCudg6dUgfHjjU@taxi-cluster.i5ffecg.mongodb.net/?retryWrites=true&w=majority')

db = mongo_client['super_taxi']
drivers = db["drivers"]
bookings = db["bookings"]


def lambda_handler(event, context):
    try:
        data = json.loads(json.dumps(event))
        body = json.loads(data.get('body'))

        booking_id = body["booking_id"]

        booking_data = bookings.find_one({"_id": ObjectId(booking_id)})

        if (booking_data == None):
            return json.dumps({
                'statusCode': 404,
                'status': False,
                'message': 'Booking details not found.'
            })
        else:
            drivers.update_one(
                {"_id": booking_data["taxi_id"]}, {"$set": {"status": "ACTIVE"}})

            bookings.update_one(
                {"_id": ObjectId(booking_id)}, {"$set": {"end_date": datetime.datetime.now(), "status": "COMPLETED"}})

            return json_util.dumps({
                'statusCode': 200,
                'status': True,
                'message': 'Ride completed successfully.'
            })

    except Exception as e:
        return json.dumps({
            'statusCode': 500,
            'status': False,
            'body': json.dumps({'error': str(e)})
        })
