from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS

import random

def recommend(user_id=None, business_id=None, city_id=None, n=10):
    city = random.choice(CITIES)
    return random.sample(BUSINESSES[city], n)
