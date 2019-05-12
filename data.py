"""
This file loads the data from the data directory and shows you how.
Feel free to change the contents of this file!
Do ensure these functions remain functional:
    - get_business(city, business_id)
    - get_reviews(city, business_id=None, user_id=None, n=10)
    - get_user(username)
"""

import json
import os
import random
from typing import List

import pandas as pd


class Data:

    def __init__(self, data_directory="data"):
        """
        Initializes class
        :param data_directory: the folder with the folders with the json files
        """
        self.data_directory = data_directory

        self.CITIES: List[str] = self.load_cities()
        self.USERS = self.load(self.CITIES, "user")
        self.BUSINESSES = self.load(self.CITIES, "business")
        self.REVIEWS = self.load(self.CITIES, "review")
        self.TIPS = self.load(self.CITIES, "tip")
        self.CHECKINS = self.load(self.CITIES, "checkin")

    def load_cities(self):
        """
        Finds all cities (all directory names) in ./data

        :return: a list of city names
        """

        return [city for city in os.listdir(self.data_directory) if city.startswith(".") is False]

    def load(self, cities: list, data_filename: str):
        """
        Given a list of city names,
            for each city extract all data from ./data/<city>/<data_filename>.json
        Returns a dictionary of the form:
            {
                <city1>: [<entry1>, <entry2>, ...],
                <city2>: [<entry1>, <entry2>, ...],
                ...
            }

        :param cities: list of city names
        :param data_filename: string with name of datafile
        :return: dict of cities with data
        """
        print(cities, data_filename)

        data = {}
        for city in cities:
            city_data = []
            with open(f"{self.data_directory}/{city}/{data_filename}.json", "r") as f:
                for line in f:
                    city_data.append(json.loads(line))
            data[city] = city_data
        return data

    def get_business(self, city, business_id):
        """
        Given a city name and a business id, return that business's data.
        Returns a dictionary of the form:
            {
                name:str,
                business_id:str,
                stars:str,
                ...
            }
        :param city: string of city name
        :param business_id: string with business id
        :return: dict with data from the json files
        """
        for business in self.BUSINESSES[city]:
            if business["business_id"] == business_id:
                return business
        raise IndexError(f"invalid business_id {business_id}")

    def get_reviews(self, city, business_id=None, user_id=None, n=10):
        """
        Given a city name and optionally a business id and/or user id,
        return n reviews for that business/user combo in that city.
        Returns a dictionary of the form:
            {
                text:str,
                stars:str,
                ...
            }
        :param city:
        :param business_id:
        :param user_id:
        :param n: amount of reviews
        :return: dict with review data
        """
        def should_keep(review):
            if business_id and review["business_id"] != business_id:
                return False
            if user_id and review["user_id"] != user_id:
                return False
            return True

        reviews = self.REVIEWS[city]
        reviews = [review for review in reviews if should_keep(review)]
        return random.sample(reviews, min(n, len(reviews)))

    def get_user(self, username):
        """
        Get a user by its username
        Returns a dictionary of the form:
            {
                user_id:str,
                name:str,
                ...
            }
        :param username:
        :return: a dict with user data
        """
        for city, users in self.USERS.items():
            for user in users:
                if user["name"] == username:
                    return user
        raise IndexError(f"invalid username {username}")

    def dict_to_dataframe(self, data: dict, columns: list = None, cities: list = None) -> dict:
        """
        Converts a given json file into a DataFrame,
        Only converts given columns if columns are given else convert all

        :param data:
        :param columns:
        :param cities:
        :return: a dict with cities as keys and the values are pandas DataFrames
        """

        df_dict = {}
        cities = self.CITIES if cities is None else cities
        columns = data[cities[0]][0].keys() if columns is None else columns

        for city in cities:
            # create empty DataFrame with right columns for every city
            df_dict[city] = pd.DataFrame(columns=columns)

            for data_dict in data[city]:
                # filter json-data on given columns and append filtered dict to DataFrame
                filtered_dict = {wanted: data_dict[wanted] for wanted in columns}
                df_dict[city] = df_dict[city].append(filtered_dict, ignore_index=True)

        return df_dict
