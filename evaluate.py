import random
import numpy as np

from recommender import Recommender

rec = Recommender()

class Evaluate:
    
    def split_data(self, data, d = 0.5):
        """ 
        Split data in a training and test set 
        'd' is the fraction of data in the training set
        """
        np.random.seed(seed=5)
        mask_test = np.random.rand(data.shape[0]) < d
        return data[mask_test], data[~mask_test]

    def mse(self, predicted_ratings):
        """Computes the mean square error between actual ratings and predicted ratings

        Arguments:
        predicted_ratings -- a dataFrame containing the columns rating and predicted rating
        """
        diff = sum(predicted_ratings['stars'].sub(predicted_ratings['predicted stars']) ** 2)
        return (diff / len(predicted_ratings))


    def mse_item_based(self, n):
        mse_list = []
        for _ in range(n):
            city = random.choice(rec.data.CITIES)
            training, test = self.split_data(rec.data.dict_to_dataframe(rec.data.REVIEWS, city, columns=["user_id", "business_id",
                                                                                                        "stars", "date"]))
            
            utility_matrix = rec.data.pivot_stars(training, city)
            adj_sim_matrix = rec.mean_centered(utility_matrix)
            while True:
                user_id = random.choice(test['user_id'].values)
                if user_id in training['user_id'].values:
                    break
            
            predicted = test[test['user_id'] == user_id].reset_index()
            
            for index, business_id in enumerate(predicted['business_id']):

                try:
                    neighbourhood = rec.neighbourhood(adj_sim_matrix, utility_matrix, user_id, business_id)

                    predicted.loc[index, 'predicted stars'] = sum(utility_matrix[user_id].mul(neighbourhood).dropna()) / sum(
                        neighbourhood.dropna())

                except ZeroDivisionError:
                    predicted.loc[index, 'predicted stars'] = np.nan
            
            mse_list.append(self.mse(predicted))
        return mse_list

print(Evaluate().mse_item_based(10))
