from model import MALModel
from view import MALView


class MALController:
    """Controller for the application."""
    def __init__(self):
        self.view= MALView(self)
        self.model = MALModel()

    def back_button_handler(self, location):
        if location == 'InfoPage1':
            self.view.explore_page()
        elif location == 'InfoPage2':
            self.view.info_page1(self.view.row)
        elif location == 'DataPage':
            self.view.explore_page()

    def get_descriptive_data(self):
        return self.model.descriptive_score()

    def search_button_clicked(self):
        """Handler for the search button click event"""
        keyword = self.view.search_keyword.get()
        matching_anime = self.search_anime(keyword)
        self.view.populate_listbox(matching_anime)

    def search_anime(self, keyword):
        """Search for anime based on user input."""
        anime_names = self.model.df['Name'].tolist()
        matching_anime = [name for name in anime_names if keyword.lower() in name.lower()]
        return matching_anime

    def get_other_name(self, anime_name):
        """Get the 'Other Name' based on the anime name"""
        row = self.model.df[self.model.df['Name'] == anime_name]
        other_name = row['Other name'].values[0] if not row.empty else ''
        return other_name

    def row_selected(self, anime_name):
        """Handler for when a row is selected"""
        row = self.model.df[self.model.df['Name'] == anime_name]
        return row

    def run(self):
        self.view.run()
