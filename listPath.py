from constants import *
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

listPathShip = [(resource_path("assets/images/ship2.png"), (FIELD_COORD[0] + 3, FIELD_COORD[1] + 3), 1),
               (resource_path("assets/images/ship3.png"), (FIELD_COORD[0] + 3 + CELL_SIZE[0]*1, FIELD_COORD[1] + 3), 2),
               (resource_path("assets/images/ship3.png"), (FIELD_COORD[0] + 3 + CELL_SIZE[0]*2, FIELD_COORD[1] + 3), 3),
               (resource_path("assets/images/ship4.png"), (FIELD_COORD[0] + 3 + CELL_SIZE[0]*3, FIELD_COORD[1] + 3), 4),
               (resource_path("assets/images/ship5.png"), (FIELD_COORD[0] + 3 + CELL_SIZE[0]*4, FIELD_COORD[1] + 3), 5),
               ]

listPathTopedoA = [resource_path("assets/images/Torpedo_1.png"),
                resource_path("assets/images/Torpedo_2.png"),
                resource_path("assets/images/Torpedo_3.png"),
                resource_path("assets/images/Torpedo_4.png"),
                resource_path("assets/images/Torpedo_5.png"),
                resource_path("assets/images/Torpedo_6.png"),
                resource_path("assets/images/Torpedo_7.png"),
                resource_path("assets/images/Torpedo_8.png"),
                   ]
pathImageTorpedo = [resource_path("assets/images/Torpedo_correct.png"),resource_path("assets/images/Torpedo_incorrect.png")]