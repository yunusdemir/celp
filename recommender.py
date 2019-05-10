from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS

import random

def recommend(user_id=None, business_id=None, city=None, n=10):
    """
    Returns n recommendations as a list of dicts.
    Optionally takes in a user_id, business_id and/or city.
    A recommendation is a dictionary in the form of:
        {
            business_id:str
            stars:str
            name:str
            city:str
            adress:str
        }
    """
    if not city:
        city = random.choice(CITIES)

    if business_id:
        print(next(business['categories'] for business in BUSINESSES[city] if business['business_id'] == business_id))
    
    count = []
    for city in CITIES:
        count = count + [user['review_count'] for user in USERS[city]]
    
    print('ratings pp =', sum(count) / sum([len(USERS[town]) for town in CITIES]))
    print('businesses =', sum([len(BUSINESSES[city]) for city in CITIES]))
    print('users =', sum([len(USERS[city]) for city in CITIES]))
    print('cities =', [city for city in CITIES])
    return random.sample(BUSINESSES[city], n)

