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

        if not business_id and not user_id:
            return self.index_not_logged_in()

        elif not business_id and user_id:
            return self.index_logged_in(user_id)

        elif business_id and city:
            return self.business_page(business_id, city)

        elif business_id:
            df_total = self.data.BUSINESSES[city]
            df = self.data.dict_to_dataframe(self.data.BUSINESSES[city],
                                             ["business_id", "categories"])
            matrix = self.create_similarity_matrix_categories(df)
            list_recommend = self.top_similarity(matrix, city, business_id)
            trimmed_list = [item for item in list_recommend if next(
                (business['city'] for business in df_total if business['business_id'] == item),
                None).lower() == city]
            print(len(trimmed_list))
            return [self.data.get_business(city, b_id) for b_id in trimmed_list]

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
    def top_similarity(df: pd.DataFrame, business_id: str, n: int = 10,
                       min_sim: float = 0.25) -> list:
        """
        Function to get the top n similar businesses with highest similarities

        :param df: DataFrame from create_similarity_matrix_categories
        :param business_id: the id of the business to test for similarity
        :param n: maximum length of returned list
        :param min_sim: minimum similarity
        :return: list of business_id's where the similarity is at least 0.25
        """
        sim_series = df.loc[business_id].drop(business_id)

        similarities = sim_series.unique()
        similarities = [value for value in similarities if value >= min_sim]
        similarities = np.sort(similarities)[::-1]

        top_list = list()

        for similarity in similarities:
            top_list += [item for item in sim_series.index if sim_series[item] >= similarity]

            if len(top_list) >= n:
                break

        return random.sample(top_list, n) if len(top_list) > n else top_list

    def index_not_logged_in(self) -> list:
        """
        Function that returns businesses and data when user visit homepage and is not logged in

        :return: list with all data of businesses
        """

        return_best = list()

        for _ in range(9):
            city = random.choice(self.data.CITIES)
            all_data = self.data.BUSINESSES[city]

            best_of_all = [item for item in all_data if item['stars'] >= 4 and item[
                'review_count'] >= 15]

            return_best.append(random.choice(best_of_all))

        return return_best

    def business_page(self, business_id, city) -> list:
        """
        Function that returns other similar businesses on the business page

        :param business_id: id of the business of the page
        :param city: city that the business is in
        :return: list of all data of similar businesses
        """
        df = self.data.dict_to_dataframe(self.data.BUSINESSES[city], ["business_id", "categories"])
        sim_matrix = self.create_similarity_matrix_categories(df)
        top_sim = self.top_similarity(sim_matrix, business_id)

        return [self.data.get_business(city, b_id) for b_id in top_sim]

    def index_logged_in(self, user_id) -> list:
        # choose random city of users city
        city = random.choice(self.data.get_cities_by_user_id(user_id))

        df_reviews = self.data.dict_to_dataframe(self.data.REVIEWS[city],
                                                 ["business_id", "stars"])

        # create similarity matrix with mean centered ratings
        utility_matrix = self.data.pivot_stars(city)
        mean_centered_utility_matrix = utility_matrix.sub(utility_matrix.mean())
        similarity_matrix = self.data.similarity_matrix_cosine(mean_centered_utility_matrix)

        # create list of businesses that user hasn't rated yet
        not_rated = [review['business_id'] for review in self.data.REVIEWS[city] if
                     review['user_id'] != user_id]

        for index, business_id in enumerate(not_rated):
            neighbourhood = self.neighbourhood(similarity_matrix, utility_matrix,
                                               user_id, business_id)
            try:
                df_reviews.at[index, 'predicted rating'] = sum(
                    utility_matrix[user_id].mul(neighbourhood).dropna()) / sum(
                    neighbourhood.dropna())
            except ZeroDivisionError:
                df_reviews.at[index, 'predicted rating'] = np.nan 
        print(df_reviews)

    @staticmethod
    def neighbourhood(similarity_matrix: pd.DataFrame, utility_matrix: pd.DataFrame, user_id: str,
                      new_business: str) -> pd.Series:
        """
        Returns Series with business IDs as index and similarity with given business as value
        Filters out businesses that user has already rated and businesses with similarity below 0
        """
        visited = utility_matrix[user_id].dropna().index

        return similarity_matrix[new_business][(similarity_matrix[new_business] > 0) & (
            similarity_matrix[new_business].index.isin(visited))]


print(Recommender().index_logged_in('NfU0zDaTMEQ4-X9dbQWd9A'))