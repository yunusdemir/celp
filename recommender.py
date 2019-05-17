import random

import numpy as np
import pandas as pd

from data import Data


class Recommender:

    def __init__(self, data_directory="data"):
        self.data = Data(data_directory)

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

        city = random.choice(self.data.CITIES) if not city else city

        if not business_id:
            return_best = []
            for _ in range(9):
                city = random.choice(self.data.CITIES)
                all_data = self.data.BUSINESSES[city]
                
                best_of_all = [item for item in all_data if item['stars'] >= 4 and item['review_count'] >= 15]

                return_best.append(random.choice(best_of_all))
            return return_best

            if user_id:
                print('USER')
                # choose random city of users city
                city = random.choice(Data().get_city_by_user_id(user_id))

                df_reviews = self.data.dict_to_dataframe(self.data.REVIEWS[city],
                                                         ["business_id", "stars"])
                
                # make similarity matrix wit mean centered ratings
                utility_matrix = Data().pivot_stars(city)
                mean_centered_utility_matrix = utility_matrix.sub(utility_matrix.mean())
                similarity_matrix = Data().similarity_matrix_cosine(mean_centered_utility_matrix)
                
                # make list of businesses that user hasn't rated yet
                not_rated = [review['business_id'] for review in self.data.REVIEWS[city] if review['user_id'] != user_id]

                for business_id in not_rated:
                    neighborhood = self.neighborhood(similarity_matrix, mean_centered_utility_matrix, user_id, business_id)
                    df_reviews['predicted rating'] = sum(mean_centered_utility_matrix[user_id].mul(neighborhood).dropna()) / sum(neighborhood.dropna())
                print(df_reviews)

        elif business_id:
            df = self.data.dict_to_dataframe(self.data.BUSINESSES[city],
                                             ["business_id", "categories"])
            matrix = self.create_similarity_matrix_categories(df)
            list_recommend = self.top_similarity(matrix, business_id)

            return [self.data.get_business(city, b_id) for b_id in list_recommend]

    
    def create_similarity_matrix_categories(self, df_data: pd.DataFrame) -> pd.DataFrame:
        """
        Create a similarity matrix for categories

        :param df_data: DataFrame with at least the columns "business_id" and "categories"
        :return: similarity matrix based on categories
        """

        df = self.data.extract_categories(df_data)
        df_utility_categories = self.data.pivot_categories(df)

        npu = df_utility_categories.values
        m1 = npu @ npu.T
        m2 = m1 / np.diag(m1)
        m3 = np.minimum(m2, m2.T)
        return pd.DataFrame(m3, index=df_utility_categories.index,
                            columns=df_utility_categories.index)
    
    @staticmethod
    def top_similarity(df: pd.DataFrame, business_id: str, n: int = 10) -> list:
        """
        Function to get the top n similair businesses

        :param df: DataFrame from create_similarity_matrix_categories
        :param business_id: the id of the business to test for similarity
        :param n: maximum length of returned list
        :return: list of business_id's where the similarity is at least 0.25
        """
        sim_series = df.loc[business_id].drop(business_id)
        sim_list = [item for item in sim_series.index if sim_series[item] >= 0.25]

        return random.sample(sim_list, n) if len(sim_list) > n else sim_list

    def neighborhood(self, similarity_matrix: pd.DataFrame, utility_matrix: pd.DataFrame, user_id: str, new_business: str) -> pd.Series:
        """
        Returns Series with business IDs as index and similarity with given business as value
        Filters out businesses that user has already rated and businesses with similarity below 0
        """
        visited = utility_matrix[user_id].dropna().index

        return similarity_matrix[new_business][(similarity_matrix[new_business] > 0) & (similarity_matrix[new_business].index.isin(visited))]