import pymongo
import json
from bson import json_util, ObjectId
import datetime

mongo_client = pymongo.MongoClient(
    'mongodb+srv://team_raghav:mZaCudg6dUgfHjjU@taxi-cluster.i5ffecg.mongodb.net/?retryWrites=true&w=majority')

db = mongo_client['super_taxi']
collection = db["bookings"]
users_collection = db["users"]
drivers_collection = db["drivers"]


# AWS_REGION = 'us-east-1'
# sns_client = boto3.client('sns', aws_access_key_id="AKIAVKYQB4TVCRDCQLKY",
#                           aws_secret_access_key="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", region_name=AWS_REGION)

def lambda_handler(event, context):
    try:
        data = json.loads(json.dumps(event))
        body = json.loads(data.get('body'))

        phone_number = body["phone_number"]
        drop_off_location = body["drop_off_location"]
        vehicle_type = body["vehicle_type"]
        taxi_id = body["taxi_id"]

        user_data = users_collection.find_one({"phone_number": phone_number})
        # taxi_data = drivers_collection.find_one({"_id": ObjectId(taxi_id)})

        if user_data == None:
            return json.dumps({
                "statusCode": 404,
                "status": False,
                "message": "User not found."
            })
        else:

            # if taxi_data["subscription_arn"] != None:
            #     sns_client.subscribe(
            #         TopicArn=taxi_data["subscription_arn"],
            #         Protocol='email',
            #         Endpoint=email,
            #         ReturnSubscriptionArn=True
            #     )

            user_data = dict(user_data)

            drivers_collection.update_one(
                {"_id": ObjectId(taxi_id)},
                {
                    '$set': {
                        "status": "BOOKED"
                    }
                }
            )

            booking_data = {
                "user_id": user_data["_id"],
                "taxi_id": ObjectId(taxi_id),
                "pickup_location": user_data["location"],

                "phone_number": phone_number,
                "drop_off_location": drop_off_location,
                "vehicle_type": vehicle_type,
                "status": "ONGOING",
                "start_date": datetime.datetime.now()
            }

            insert_booking = collection.insert_one(booking_data)

            return json_util.dumps({
                "statusCode": 201,
                "status": True,
                "message": "Booking created successfully.",
                "booking_id": str(insert_booking.inserted_id)
            })
    except Exception as e:
        return json.dumps({
            'statusCode': 500,
            'status': False,
            'body': json.dumps({'error': str(e)})
        })
