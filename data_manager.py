import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class DataManager:
    def __init__(self):
        pass

    @staticmethod
    def load_data(filepath):
        """Load data from CSV file"""
        df = pd.read_csv(filepath)

        return df
