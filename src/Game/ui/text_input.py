from game.ui import button

class Input(button.Button):
    def __init__(self, text=None, label=None, label_direction = "left", box_size:tuple=(0,0), char_limit=10, color="WHITE"):
        