import os
import logging
import requests
import json
import pandas as pd
import numpy as np


class SteelEyeExercise:
    """
    Class permits to load json files from an url. 
    Custom logic to calculate the target columns using pandas dataframes.
    Final export of a CSV file with the target dataframe requested.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
        self.main()

    def main(self) -> None:
        """
        Main function that reads the input json files and writes the output csv file
        """
        country_json = self.load_file(
            'https://api.nobelprize.org/v1/country.json')
        country_values = country_json.get('countries')

        laureate_file = self.load_file(
            'https://api.nobelprize.org/v1/laureate.json')
        laureate_values = laureate_file.get('laureates')

        self.logger.info('Transformation to dataframes.')
        self.df_country = pd.DataFrame.from_dict(country_values)
        df_laureate = pd.DataFrame.from_dict(laureate_values)

        self.logger.info('Start custom logic.')
        df = df_laureate.copy()

        df['name'] = np.where(
            df['gender'] == 'org', df['firstname'], (df['firstname'] + ' ' + df['surname']))
        df.rename(columns={'born': 'dob'}, inplace=True)

        df['unique_prize_years'] = df['prizes'].map(
            lambda x: self.get_unique_prize_years(x))
        df['unique_prize_categories'] = df['prizes'].map(
            lambda x: self.get_unique_prize_categories(x))
        df['country_name'] = df['bornCountryCode'].map(
            lambda x: self.get_country_name(x, self.df_country))

        df = df[['id', 'name', 'dob', 'unique_prize_years',
                 'unique_prize_categories', 'gender', 'country_name']]

        self.logger.info(
            'Converting to CSV. File SteelEyeExercise.csv will be saved in current directory.')
        #default utf-8 encoding doesn't cover all symbols in the final file
        df.to_csv('SteelEyeExercise.csv', index=False)

    def get_country_name(self, x, df_country) -> str:
        """
            Get country name from country code
            :param x: country code
            :type x: string
            :param df_country: dataframe with both country name and code
            :type df_country: dataframe
            :return: random match for the code or None
            :rtype: string
        """
        result = df_country.loc[df_country['code'] == x, 'name']
        return None if len(result) == 0 else result.iloc[0]

    def get_unique_prize_categories(self, x) -> str:
        """
            Get unique prize categories separated by ;
            :param x: list containing a dict of prizes
            :type x: list of dict
            :return: categories separated by ;
            :rtype: string
        """
        result = []
        for i in range(len(x)):
            result.append(x[i].get('category'))
        #using set for uniqueness
        result = set(result)
        return ';'.join(str(s) for s in result)

    def get_unique_prize_years(self, x) -> str:
        """
            Get unique prize years separated by ;
            :param x: list containing a dict of prizes
            :type x: list of dict
            :return: years separated by ;
            :rtype: string
        """
        result = []
        for i in range(len(x)):
            result.append(x[i].get('year'))
        #using set for uniqueness
        result = set(result)
        return ';'.join(str(s) for s in result)

    def load_file(self, url) -> json:
        """
            Load json file from url
            :param url: url to load file from
            :type url: string
            :return: json object.
            :rtype: json
        """
        self.logger.info('Loading file from url: ' + url)
        try:
            r = requests.get(url, allow_redirects=True)
        except requests.HTTPError as e:
            self.logger.error(e)
        return r.json()
