import random

from data import Data


class Recommender:

    def __init__(self):
        self.data = Data()

    def recommend(self, user_id=None, business_id=None, city=None, n=10):
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
            city = random.choice(self.data.CITIES)
        return random.sample(self.data.BUSINESSES[city], n)
