"""model"""
from data_manager import DataManager


class MALModel:
    def __init__(self):
        self.df = DataManager.load_data('anime-dataset-2023.csv')

    def descriptive_score(self):
        filtered_scores = self.df[self.df['Score'] != 'UNKNOWN']['Score']

        min_score = filtered_scores.min()
        max_score = filtered_scores.max()
        average_score = filtered_scores.astype(float).mean()
        mode_score = filtered_scores.mode()

        if not mode_score.empty:
            mode_score = mode_score.iloc[0]

        list_data = [min_score, max_score, average_score, mode_score]
        return list_data
