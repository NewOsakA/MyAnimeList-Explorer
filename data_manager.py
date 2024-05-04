"""Manage the data"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


class DataManager:
    def __init__(self):
        pass

    @staticmethod
    def load_data(filepath):
        """Load data from CSV file"""
        df = pd.read_csv(filepath)
        return df

    @staticmethod
    def dict_transform(row):
        row_dict = row.to_dict(orient='records')
        return row_dict[0]

    @staticmethod
    def combine_source_types(df):
        # Define mappings for combining similar source types
        source_mapping = {
            'Visual novel': 'Novel',
            'Light novel': 'Novel',
            'Web novel': 'Novel',
            '4-koma manga': 'Manga',
            'Manga': 'Manga',
            'Web manga': 'Manga',
            'Original': 'Original',
            'Book': 'Other',
            'Mixed media': 'Other',
            'Music': 'Other',
            'Other': 'Other',
            'Picture book': 'Other',
            'Radio': 'Other',
            'Unknown': 'Other'
        }

        # Replace source types according to the mapping
        df['Source'] = df['Source'].map(source_mapping)

        # Group by the updated source types and sum up the scores
        # df = df.groupby('Source').sum().reset_index()
        return df

    @staticmethod
    def story_bar(df):
        # Filter out 'UNKNOWN' values in the 'Score' column
        filtered_df = df[df['Score'] != 'UNKNOWN']

        # Convert 'Score' column to numeric (if it's not already numeric)
        filtered_df.loc[:, 'Score'] = pd.to_numeric(filtered_df['Score'], errors='coerce')
        avg_scores = filtered_df.groupby('Source')['Score'].mean().reset_index().sort_values(by='Score',
                                                                                             ascending=False)

        fig = Figure(figsize=(2, 2))
        ax = fig.add_subplot(111)

        # Plotting the bar plot
        bar_plot = sns.barplot(x='Source', y='Score', data=avg_scores, ax=ax)

        # Customizing colors
        colors = ['#27408B', '#008080', '#71C671', '#FFA07A']
        for i, bar in enumerate(bar_plot.patches):
            bar.set_color(colors[i % len(colors)])

        ax.set_title('Average Score by Source Type', fontsize=6)
        ax.set_xlabel('Source Type', fontsize=6)
        ax.set_ylabel('Average Score', fontsize=6)
        ax.tick_params(axis='both', which='major', labelsize=6)
        plt.xticks(rotation=45, ha='right')
        fig.tight_layout(pad=0.5)

        return fig

    @staticmethod
    def story_scatter(df):
        # Filter out 'UNKNOWN' values in the 'Score' column
        filtered_df = df[df['Score'] != 'UNKNOWN']

        # Convert 'Score' column to numeric (if it's not already numeric)
        filtered_df.loc[:, 'Score'] = pd.to_numeric(filtered_df['Score'], errors='coerce')

        fig = Figure(figsize=(2, 2))
        ax = fig.add_subplot(111)

        # Plotting the scatter plot
        scatter_plot = sns.scatterplot(x='Source', y='Score', data=filtered_df, ax=ax, s=50)

        ax.set_title('Score Comparison by Source Type', fontsize=6)
        ax.set_xlabel('Source Type', fontsize=6)
        ax.set_ylabel('Score', fontsize=6)
        ax.tick_params(axis='both', which='major', labelsize=6)
        plt.xticks(rotation=45, ha='right')

        fig.tight_layout(pad=0.5)

        return fig

    @staticmethod
    def story_heatmap(df):
        # Filter out 'UNKNOWN' values in the 'Score' column
        filtered_df = df[df['Score'] != 'UNKNOWN']

        # Convert 'Score' column to numeric (if it's not already numeric)
        filtered_df.loc[:, 'Score'] = pd.to_numeric(filtered_df['Score'], errors='coerce')

        # One-hot encode the 'Source' variable
        encoded_df = pd.get_dummies(filtered_df['Source'])

        # Concatenate the one-hot encoded variables with the 'Score'
        encoded_df['Score'] = filtered_df['Score']

        # Calculate the correlation matrix
        corr_matrix = encoded_df.corr()

        fig = Figure(figsize=(2, 2))
        ax = fig.add_subplot(111)

        # Plotting the heatmap
        heatmap = sns.heatmap(corr_matrix, cmap='coolwarm', annot=True, ax=ax, square=True)

        ax.set_title('Correlation Heatmap of Average Score and Source Type', fontsize=6)
        ax.set_xlabel('Source type and Score', fontsize=6)
        ax.set_ylabel('Source type and Score', fontsize=6)
        ax.tick_params(axis='both', which='major', labelsize=6)

        fig.tight_layout(pad=0.5)

        return fig

    @staticmethod
    def story_histogram(df, selected_source):
        # Filter the DataFrame for the selected source type
        selected_df = df[df['Source'] == selected_source]

        # Filter out 'UNKNOWN' values in the 'Score' column
        filtered_df = selected_df[selected_df['Score'] != 'UNKNOWN']

        # Convert 'Score' column to numeric (if it's not already numeric)
        filtered_df.loc[:, 'Score'] = pd.to_numeric(filtered_df['Score'], errors='coerce')

        fig = Figure(figsize=(1.25, 2.5))
        ax = fig.add_subplot(111)

        # Plotting the histogram
        histogram = sns.histplot(filtered_df['Score'], bins=10, kde=True, ax=ax)

        ax.set_title(f'Histogram of Scores for Source Type: {selected_source}', fontsize=6)
        ax.set_xlabel('Score', fontsize=6)
        ax.set_ylabel('Frequency', fontsize=6)
        ax.tick_params(axis='both', which='major', labelsize=6)
        ax.grid(True)

        fig.tight_layout(pad=0.5)

        return fig
