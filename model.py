"""model"""
from data_manager import DataManager


class MALModel:
    def __init__(self):
        self.df = DataManager.load_data('anime-dataset-2023.csv')

    def printtest(self):
        print(self.df.head())
