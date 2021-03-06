import random
import numpy as np
import pandas as pd

from recommender import Recommender

rec = Recommender()

class Evaluate:
    
    def mse(self, predicted_ratings) -> int:
        """
        Computes the mean square error between actual ratings and predicted ratings

        :param predicted_ratings: DataFrame containing the columns rating and predicted rating
        :return: int containing mse of given Dataframe
        """
        diff = sum(predicted_ratings['stars'].sub(predicted_ratings['predicted stars']) ** 2)
        return (diff / len(predicted_ratings))


    def mse_user(self, user_id, city, df_reviews, similarity_genres = None) -> int:
        """
        Predicts ratings for every business already rated by given user 
        and returns mse of user predictions

        :param user_id -- id of user to predict ratings for
        :param city -- city to get businesses and reviews from, needed for pivot_stars function
        :param df_reviews -- DataFrame containing all reviews of given city
        :return: int containing mse
        """
        utility_matrix = rec.data.pivot_stars(df_reviews, city)
        adj_sim_matrix = rec.mean_centered(utility_matrix) if type(similarity_genres) != pd.DataFrame else similarity_genres
        
        reviewed = df_reviews[df_reviews['user_id'] == user_id].reset_index()
        
        for index, business_id in enumerate(reviewed['business_id']):
            neighbourhood = rec.neighbourhood(adj_sim_matrix, utility_matrix, user_id, business_id)
            
            try:
                reviewed.loc[index, 'predicted stars'] = sum(utility_matrix[user_id].mul(neighbourhood).dropna()) / sum(
                    neighbourhood.dropna())
                
            except ZeroDivisionError:
                reviewed.loc[index, 'predicted stars'] = np.nan
        return self.mse(reviewed)

    def mse_item_based(self) -> dict:
        """
        Calculates mse of every city and returns mse as value with city as key

        :return: dict with cities as keys and mse's as values
        """
        mse_dict = {}

        for city in rec.data.CITIES:
            df_reviews = rec.data.dict_to_dataframe(rec.data.REVIEWS, city, columns=['user_id', 'business_id', 'stars', 'date'])
            mse_list = pd.Series([self.mse_user(user_id, city, df_reviews) for user_id in df_reviews['user_id'].values]).dropna()
            mse_dict[city] = sum(mse_list) / len(mse_list)
        return mse_dict

    def mse_content_based(self) -> dict:
        mse_dict = {}

        for city in rec.data.CITIES:
            df_reviews = rec.data.dict_to_dataframe(rec.data.REVIEWS, city, columns=['user_id', 'business_id', 'stars', 'date'])
            df_businesses = rec.data.dict_to_dataframe(rec.data.BUSINESSES, city, columns=['business_id', 'categories'])
            similarity = rec.create_similarity_matrix_categories(df_businesses)
            
            mse_list = pd.Series([self.mse_user(user_id, city, df_reviews, similarity) for user_id in df_reviews['user_id'].values]).dropna()
            mse_dict[city] = sum(mse_list) / len(mse_list)
        return mse_dict

    def mse_mean(self) -> dict:
        mse_dict = {}

        for city in rec.data.CITIES:
            df_reviews = rec.data.dict_to_dataframe(rec.data.REVIEWS, city, columns=['user_id', 'business_id', 'stars', 'date'])
            df_reviews['predicted stars'] = df_reviews['stars'].mean()
            mse_dict[city] = self.mse(df_reviews)
        return mse_dict

    def mse_random(self) -> dict:
        mse_dict = {}

        for city in rec.data.CITIES:
            df_reviews = rec.data.dict_to_dataframe(rec.data.REVIEWS, city, columns=['user_id', 'business_id', 'stars', 'date'])
            for index in df_reviews.index:
                df_reviews.loc[index, 'predicted stars'] = np.random.uniform(0.5, 5.0)
            
            mse_dict[city] = self.mse(df_reviews)
        return mse_dict
print(Evaluate().mse_random())     