"""UI for MyAnimeList Explorer application"""
import tkinter as tk
from io import BytesIO
from tkinter import ttk

import requests
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from data_manager import DataManager


class MALView(tk.Tk):
    """UI for the MyAnimeList-Explorer application."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("MyAnimeList Explorer")
        self.minsize(width=1100, height=750)  # fix the minimum size of the screen
        self.df = DataManager.load_data('anime-dataset-2023.csv')
        self.df = DataManager.combine_source_types(self.df)
        self.search_keyword = tk.StringVar()
        self.selected_source = tk.StringVar()
        self.initial_combobox = 'Select Histogram'
        self.selected_source.set(self.initial_combobox)
        self.init_component()

    def init_component(self):
        # Color library and padding
        pure_white_bg = "#FFFFFF"
        white_bg = "#FFFAFA"
        black_bg = "#000000"
        blue_bg = "#2e51a2"
        light_blue_bg = "#CAE4FF"

        style = ttk.Style()
        style.theme_use('clam')
        # style.configure('TFrame', background=blue_bg)
        style.configure('TFrame', background=blue_bg)
        style.configure('Light.TFrame', background=light_blue_bg)
        style.configure('TLabel', background=blue_bg, foreground=white_bg, font=("Georgia", 70))
        style.configure('InfoLabel.TLabel', background=light_blue_bg, foreground=blue_bg, font=("Georgia", 40))
        style.configure('Info.TLabel', background=light_blue_bg, foreground=blue_bg, font=("Georgia", 15))
        style.configure('Info2.TLabel', background=pure_white_bg, foreground=black_bg, font=("Georgia", 20))
        style.configure('Hist.TCombobox', background=light_blue_bg, foreground=blue_bg, font=("Times New Roman", 20))
        style.configure('Custom.TButton', background=light_blue_bg, foreground=blue_bg, font=("Times New Roman", 17))

        # self.grid_rowconfigure(1, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        # top frame
        self.menu_frame = ttk.Frame(self, style="TFrame")
        self.menu_frame.grid(row=0, column=0, sticky="NSEW")
        self.menu_label = ttk.Label(self.menu_frame, text="MyAnimeList Explorer",
                                    style='TLabel', padding=(60, 10))
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

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid_rowconfigure(0, weight=0)
        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid_columnconfigure(1, weight=0)

    def create_search_comp(self):
        """Create search bar and search button"""
        self.search = ttk.Entry(self.middle_frame, width=85, textvariable=self.search_keyword)
        self.search.grid(row=0, column=0, sticky="EW", padx=10, pady=10)
        self.search.focus()

        self.search_button = ttk.Button(self.middle_frame, text="Search", command=self.controller.search_button_clicked)
        self.search_button.grid(row=0, column=1, sticky="EW", padx=10, pady=10)

    def create_listbox(self):
        """Create treeview widget"""
        columns = ('name', 'other name')
        self.list = ttk.Treeview(self.middle_frame, columns=columns, show='headings')
        self.list.grid(row=1, column=0, columnspan=2, sticky="NSEW", padx=10, pady=10)
        self.list.heading('name', text='Name')
        self.list.heading('other name', text='Other Name')
        self.list.bind("<<TreeviewSelect>>", self.on_select)  # Bind the event to the callback method

    def on_select(self, event):
        """Callback method for when a row is selected"""
        selected_item = self.list.selection()[0]  # Get the selected item
        anime_name = self.list.item(selected_item, "values")[0]  # Get the anime name from the selected item
        selected_row = self.controller.row_selected(anime_name)  # Notify the controller that a row is selected
        self.info_page1(selected_row)

    def populate_listbox(self, anime_names):
        """Populate the treeview widget with matching anime names"""
        self.list.delete(*self.list.get_children())  # Clear existing items
        for name in anime_names:
            other_name = self.controller.get_other_name(name)
            self.list.insert('', 'end', values=(name, other_name))  # Insert anime name into the treeview

    def create_set_button(self):
        """Create interactive buttons at the bottom of the screen"""
        nav_buttons = ['Explore', 'Data Story', 'Statistical Information', 'Characteristics Comparison', 'Exit']
        button_commands = [self.explore_page, self.data_page,
                           self.temp, self.temp, self.destroy]
        padding = {"padx": 20, "pady": 20}

        for i, (text, command) in enumerate(zip(nav_buttons, button_commands)):
            if i != 4:
                button = ttk.Button(self.bottom_frame, text=text, command=command, style="Custom.TButton")
                button.grid(row=0, column=i, sticky='ew', **padding)
                self.bottom_frame.grid_columnconfigure(i, weight=1)
            else:
                button = ttk.Button(self.bottom_frame, text=text, command=command, style="Custom.TButton"
                                    , cursor="pirate")
                button.grid(row=0, column=i, sticky='ew', **padding)
                self.bottom_frame.grid_columnconfigure(i, weight=1)

    def temp(self):
        pass

    def explore_page(self):
        """Create component for explore page"""
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid_rowconfigure(0, weight=0)
        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid_columnconfigure(1, weight=0)

        self.search_keyword = tk.StringVar()  # clear the search bar input
        self.clear_middle_frame()
        self.create_search_comp()
        self.create_listbox()

    def info_page1(self, row):
        self.clear_middle_frame()
        anime = DataManager.dict_transform(row)

        self.middle_frame.grid_rowconfigure(0, weight=1)
        self.middle_frame.grid_columnconfigure(0, weight=0)
        self.middle_frame.grid_columnconfigure(1, weight=1)

        # image
        self.create_image_label(anime['Image URL'])

        # info
        info = f"Other Name: {anime['Other name']}\n" \
               f"English Name: {anime['English name']}\n" \
               f"Genres: {anime['Genres']}\n" \
               f"Aired: {anime['Aired']}\n" \
               f"Premiered: {anime['Premiered']}\n" \
               f"Score: {anime['Score']}\n\n" \
               f"Synopsis: {anime['Synopsis']}\n"

        self.info_sub_frame = ttk.Frame(self.middle_frame, style='Light.TFrame')
        self.info_sub_frame.grid(row=0, column=1, sticky='N')

        self.name = ttk.Label(self.info_sub_frame, text=anime['Name'], style="InfoLabel.TLabel", anchor=tk.CENTER
                              , wraplength=600)
        self.name.grid(row=0, column=0, padx=10, pady=(25, 0), sticky='NEW')

        self.other = ttk.Label(self.info_sub_frame, text=info, style="Info.TLabel", anchor=tk.W, wraplength=500)
        self.other.grid(row=1, column=0, padx=10, pady=10)

    def info_page2(self):
        pass

    def data_page(self):
        """Create component for data page"""
        self.clear_middle_frame()
        self.middle_top_frame = tk.Frame(self.middle_frame, bg="white")
        self.middle_top_frame.pack(side="top", fill="x", expand=False, padx=20, pady=(20, 0))
        self.middle_bottom_frame = tk.Frame(self.middle_frame, bg="white")
        self.middle_bottom_frame.pack(side="top", fill="x", expand=False, padx=20, pady=(0, 0))
        self.middle_bottom2_frame = tk.Frame(self.middle_frame, bg="white")
        self.middle_bottom2_frame.pack(side="top", fill="x", expand=False, padx=20, pady=(0, 20))

        # retrieve data from model
        data = self.controller.get_descriptive_data()

        # descriptive statistic
        descriptive_stat = ttk.Label(self.middle_top_frame,
                                     text=f'Descriptive Statistic\n'
                                          f'-----------------------\n'
                                          f'Average Score\n'
                                          f'Min: {data[0]}\n'
                                          f'Max: {data[1]}\n'
                                          f'Mean: {data[2]:.2f}\n'
                                          f'Mode: {data[3]}',
                                     style='Info2.TLabel')
        descriptive_stat.pack(side="right", fill="y", expand=True, padx=(0, 100), pady=(50, 50))

        # bar graph
        fig_bar = DataManager.story_bar(self.df)
        canvas = FigureCanvasTkAgg(fig_bar, master=self.middle_top_frame)
        canvas_widget_bar = canvas.get_tk_widget()
        canvas_widget_bar.pack(side="left", fill="both", expand=True)
        canvas.draw()

        # scatterplot graph
        fig_scatt = DataManager.story_scatter(self.df)
        canvas = FigureCanvasTkAgg(fig_scatt, master=self.middle_top_frame)
        canvas_widget_scatterplot = canvas.get_tk_widget()
        canvas_widget_scatterplot.pack(side="left", fill="both", expand=True)
        canvas.draw()

        # heatmap graph
        fig_heat = DataManager.story_heatmap(self.df)
        canvas = FigureCanvasTkAgg(fig_heat, master=self.middle_bottom_frame)
        canvas_widget_heatmap = canvas.get_tk_widget()
        canvas_widget_heatmap.pack(side="left", fill="both", expand=True)
        canvas.draw()

        self.sub_frame = tk.Frame(self.middle_bottom_frame, bg="white")
        self.sub_frame.pack(side="left", fill="x", expand=True)

        # combobox for histogram
        self.selected_source.set(self.initial_combobox)
        source_list = ['Manga', 'Novel', 'Original', 'Other']
        story_combobox = ttk.Combobox(self.sub_frame, textvariable=self.selected_source,
                                      values=source_list, state="readonly", width=20, style="Hist.TCombobox",
                                      cursor="exchange")
        story_combobox.pack(side="top", expand=False, padx=(0, 0))
        story_combobox.bind('<<ComboboxSelected>>', self.story_combobox_handler)

        # histogram graph
        self.fig_hist = DataManager.story_histogram(self.df, 'Manga')
        canvas = FigureCanvasTkAgg(self.fig_hist, master=self.sub_frame)
        canvas.draw()
        self.canvas_widget_histogram = canvas.get_tk_widget()
        self.canvas_widget_histogram.pack(side="top", fill="both", expand=True)

        # conclusion
        summary = ttk.Label(self.middle_bottom2_frame,
                            text='From the graph, we can slightly see that people in the community like '
                                 'anime that made from manga the most.',
                            style='Info2.TLabel')
        summary.pack(side="left", fill="both", expand=True, padx=100)

    def story_combobox_handler(self, event):
        """Handle combobox selection."""
        selected_var = self.selected_source.get()
        if selected_var != self.initial_combobox:
            self.update_histogram(selected_var)

    def update_histogram(self, selected_var):
        """Update the histogram"""
        self.canvas_widget_histogram.destroy()
        self.fig_hist = DataManager.story_histogram(self.df, selected_var)
        canvas = FigureCanvasTkAgg(self.fig_hist, master=self.sub_frame)
        canvas.draw()
        self.canvas_widget_histogram = canvas.get_tk_widget()
        self.canvas_widget_histogram.pack(side="top", fill="both", expand=True)

    def clear_middle_frame(self):
        """Clear all middle frame component"""
        for widget in self.middle_frame.winfo_children():
            widget.destroy()

    def create_image_label(self, image_url):
        """Create a label to display the image"""
        image = self.load_image(image_url)
        label = tk.Label(self.middle_frame, image=image)
        label.image = image  # keep a reference to the image to prevent garbage collection
        label.grid(row=0, column=0, padx=30, pady=30)

    def load_image(self, image_url):
        """Load and resize the image"""
        response = requests.get(image_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((390, 530))
        return ImageTk.PhotoImage(img)

    def run(self):
        """Run the program"""
        self.mainloop()
