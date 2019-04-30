import os
import json
import random

DATA_DIR = "data"


def load_cities():
    return os.listdir(DATA_DIR)


def load(cities, data_filename):
    data = {}
    for city in cities:
        city_data = []
        with open(f"{DATA_DIR}/{city}/{data_filename}.json", "r") as f:
            for line in f:
                city_data.append(json.loads(line))
        data[city] = city_data
    return data


def get_business(city, business_id):
    for business in BUSINESSES[city]:
        if business["business_id"] == business_id:
            return business
    raise IndexError(f"invalid business_id {business_id}")


def get_reviews(city, business_id=None, user_id=None, n=10):
    def should_keep(review):
        if business_id and review["business_id"] != business_id:
            return False
        if user_id and review["user_id"] != user_id:
            return False
        return True

    reviews = REVIEWS[city]
    reviews = [review for review in reviews if should_keep(review)]
    return random.sample(reviews, min(n, len(reviews)))


CITIES = load_cities()
USERS = load(CITIES, "user")
BUSINESSES = load(CITIES, "business")
REVIEWS = load(CITIES, "review")
TIPS = load(CITIES, "tip")
CHECKINS = load(CITIES, "checkin")
