from model import MALModel
from view import MALView


class MALController:
    """Controller for the Puppy Picker application."""
    def __init__(self):
        self.model = MALModel()
        self.view = MALView(self)

    def run(self):
        self.view.run()
