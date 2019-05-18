import random

from recommender import Recommender

rec = Recommender()

class Evaluate:

    def mse(self, predicted_ratings):
        """Computes the mean square error between actual ratings and predicted ratings

        Arguments:
        predicted_ratings -- a dataFrame containing the columns rating and predicted rating
        """
        diff = predicted_ratings['stars'] - predicted_ratings['predicted stars']
        return (diff ** 2).mean()


    def item_based_filtered(self, user_id):
        return rec.predict_rating(user_id, 4)


    def mse_item_based(self, n):
        mse_list = []
        for _ in range(n):
            city = random.choice(rec.data.CITIES)
            user = random.choice(rec.data.USERS[city])
            mse_list.append(self.mse(self.item_based_filtered(user["user_id"])))


Evaluate().mse_item_based(3)
