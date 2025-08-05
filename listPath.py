import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path).replace("\\","/")

listPathImageMenuScreen = [[resource_path("assets/images/mainscreen/mainscreen_1.png")],
                            ]