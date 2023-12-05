import json
from pymongo import MongoClient, GEOSPHERE, GEO2D
from bson import ObjectId
from bson.son import SON
import pprint
import math
import time
import random
from geopy.distance import great_circle

db_uri = 'mongodb+srv://team_raghav:mZaCudg6dUgfHjjU@taxi-cluster.i5ffecg.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(db_uri)
db = client["super_taxi"]
taxis = db["drivers"]
customers = db["users"]
bookings = db["bookings"]

with open(r'./drivers.json') as file:
    taxi_list = json.load(file)


with open(r'./users.json') as file:
    customer_list = json.load(file)

driver_doc_count = customers.count_documents({})
user_doc_count = customers.count_documents({})

rec = taxis.delete_many({})
rec = taxis.insert_many(taxi_list)
taxis.create_index([('initial_location', GEOSPHERE)])
taxis.create_index([('current_location', GEOSPHERE)])

rec = customers.delete_many({})
rec = customers.insert_many(customer_list)
customers.create_index([('location', GEOSPHERE)])

print('######################## ALL TAXIS WITHIN 1 KILOMETER ########################')

# Check Once
customer_loc = customer_list[0]['location']

range_query = {
    'current_location': SON([
        ("$near", {
            "$geometry": customer_loc,
            "$maxDistance": 1000  # 1 kilometer in meters
        })
    ])
}

for doc in taxis.find(range_query):
    pprint.pprint(doc)

print('######################## THE 1 NEAREST TAXI ########################')
nearest_query = taxis.find(range_query).limit(1)

for taxi in nearest_query:
    print("Nearest Taxi:")
    print(taxi)

document = taxi

# Booking File


def booking_table_insertion():
    inserted_booking = bookings.insert_one(document)
    print("Record Inserted in Booking Table")
    fetch_inserted_document = bookings.find_one(
        {"_id": inserted_booking.inserted_id})

    return fetch_inserted_document


booking = booking_table_insertion()
print('*' * 40, booking)

# Generate Random Coordinates File


def generate_random_coordinates(current_lat, current_lng, radius_km):
    earth_radius_km = 9371.0

    current_lat_rad = math.radians(current_lat)
    current_lng_rad = math.radians(current_lng)

    u = random.uniform(0, 1)
    v = random.uniform(0, 1)
    w = radius_km * math.sqrt(u)
    t = 2 * math.pi * v

    new_lat_rad = current_lat_rad + (w / earth_radius_km) * math.cos(t)
    new_lng_rad = current_lng_rad + (w / earth_radius_km) * math.sin(t)

    new_lat = math.degrees(new_lat_rad)
    new_lng = math.degrees(new_lng_rad)

    return new_lat, new_lng


for taxi in taxis.find():
    current_lat, current_lng = taxi['current_location']['coordinates']

    radius_km = 10

    new_lat, new_lng = generate_random_coordinates(
        current_lat, current_lng, radius_km)

    taxi_id_str = str(taxi["_id"])

    previous_data = {
        "vehicle_number": taxi["vehicle_number"],
        "phone_number": taxi["phone_number"],
        "full_name": taxi["full_name"],
        "vehicle_type": taxi["vehicle_type"],
        "current_location": {
            "type": "Point",
            "coordinates": [current_lat, current_lng]
        },
        "date_of_register": taxi["date_of_register"],
        "status": taxi["status"],
        "email": taxi["email"]
    }

    updated_data = {
        "vehicle_number": taxi["vehicle_number"],
        "phone_number": taxi["phone_number"],
        "full_name": taxi["full_name"],
        "vehicle_type": taxi["vehicle_type"],
        "current_location": {
            "type": "Point",
            "coordinates": [new_lat, new_lng]
        },
        "date_of_register": taxi["date_of_register"],
        "status": taxi["status"],
        "email": taxi["email"]
    }

    print("Previous Data:")
    print(json.dumps(previous_data, indent=4))

    print("Updated Data:")
    print(json.dumps(updated_data, indent=4))

    update_query = {
        '$set': {
            'current_location.coordinates': [new_lat, new_lng]
        }
    }
    taxis.update_one({'_id': taxi['_id']}, update_query)

    print('-' * 50)
