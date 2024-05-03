"""UI for MyAnimeList Explorer application"""
import tkinter as tk
from tkinter import ttk
from data_manager import DataManager


class MALView(tk.Tk):
    """UI for the MyAnimeList-Explorer application."""
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("MyAnimeList Explorer")
        self.minsize(width=1000, height=750)  # fix the minimum size of the screen
        self.df = DataManager.load_data('anime-dataset-2023.csv')
        self.init_component()

    def init_component(self):
        # Color library and padding
        white_bg = "#FFFAFA"
        blue_bg = "#2e51a2"
        light_blue_bg = "#CAE4FF"



        style = ttk.Style()
        style.theme_use('clam')
        # style.configure('TFrame', background=blue_bg)
        style.configure('TFrame', background=blue_bg)
        style.configure('Light.TFrame', background=light_blue_bg)
        style.configure('TLabel', background=blue_bg, foreground=white_bg, font=("Georgia", 70))

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # top frame
        self.menu_frame = ttk.Frame(self, style="TFrame")
        self.menu_frame.grid(row=0, column=0, sticky="NSEW")
        self.menu_label = ttk.Label(self.menu_frame, text="MyAnimeList Explorer",
                                    style='TLabel', padding=(60, 0))
        self.menu_label.pack()

        # middle frame
        self.middle_frame = ttk.Frame(self, style="Light.TFrame", height=2)
        self.middle_frame.grid(row=1, column=0, sticky="NSEW")
        self.middle_frame.grid_rowconfigure(1, weight=1)
        self.middle_frame.grid_columnconfigure(1, weight=1)

        self.create_search_comp()
        self.create_listbox()


        # bottom frame
        self.bottom_frame = ttk.Frame(self, style="Right.TFrame")
        self.bottom_frame.grid(row=3, column=0, sticky="NSEW")
        self.create_set_button()

    def create_search_comp(self):
        """Create search bar and search button"""
        self.search = tk.Text(self.middle_frame, bg="white", height=2)
        self.search.grid(row=0, column=0, sticky="EW", padx=10, pady=10)

        self.search_button = tk.Button(self.middle_frame, text="Search")
        self.search_button.grid(row=0, column=1, sticky="EW", padx=10, pady=10)

    def create_listbox(self):
        """Create treeview widget"""
        columns = ('first_name', 'last_name', 'email')
        self.list = ttk.Treeview(self.middle_frame, columns=columns, show='headings')
        self.list.grid(row=1, column=0, columnspan=2, sticky="NSEW", padx=10, pady=10)
        self.list.heading('first_name', text='First Name')
        self.list.heading('last_name', text='Last Name')
        self.list.heading('email', text='Email')

    def create_set_button(self):
        """Create interactive buttons at the bottom of the screen"""
        nav_buttons = ['Explore', 'Data Story', 'Statistical Information', 'Characteristics Comparison', 'Exit']
        button_commands = [self.explore_page, self.data_page, self.temp, self.temp, self.destroy]
        padding = {"padx": 20, "pady": 20}

        for i, (text, command) in enumerate(zip(nav_buttons, button_commands)):
            button = ttk.Button(self.bottom_frame, text=text, command=command)
            button.grid(row=0, column=i, sticky='ew', **padding)
            self.bottom_frame.grid_columnconfigure(i, weight=1)

    def temp(self):
        pass

    def explore_page(self):
        """Create component for explore page"""
        self.clear_middle_frame()
        self.create_search_comp()
        self.create_listbox()

    def data_page(self):
        """Create component for data page"""
        self.clear_middle_frame()

    def clear_middle_frame(self):
        """Clear all middle frame component"""
        for widget in self.middle_frame.winfo_children():
            widget.destroy()

    def run(self):
        """Run the program"""
        self.mainloop()
