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

listPathTopedoA = [resource_path("assets/images/torpedo_animation/frame_00.png"),
                resource_path("assets/images/torpedo_animation/frame_01.png"),
                resource_path("assets/images/torpedo_animation/frame_02.png"),
                resource_path("assets/images/torpedo_animation/frame_03.png"),
                resource_path("assets/images/torpedo_animation/frame_04.png"),
                resource_path("assets/images/torpedo_animation/frame_05.png"),
                resource_path("assets/images/torpedo_animation/frame_06.png"),
                resource_path("assets/images/torpedo_animation/frame_07.png"),
                resource_path("assets/images/torpedo_animation/frame_08.png"),
                resource_path("assets/images/torpedo_animation/frame_09.png"),
                   ]

listPathRadarA = [resource_path("assets/images/radar_frames/frame_00.png"),
                resource_path("assets/images/radar_frames/frame_01.png"),
                resource_path("assets/images/radar_frames/frame_02.png"),
                resource_path("assets/images/radar_frames/frame_03.png"),
                resource_path("assets/images/radar_frames/frame_04.png"),
                resource_path("assets/images/radar_frames/frame_05.png"),
                resource_path("assets/images/radar_frames/frame_06.png"),
                resource_path("assets/images/radar_frames/frame_07.png"),
                resource_path("assets/images/radar_frames/frame_08.png"),
                resource_path("assets/images/radar_frames/frame_09.png"),
                resource_path("assets/images/radar_frames/frame_10.png"),
                resource_path("assets/images/radar_frames/frame_11.png"),
                resource_path("assets/images/radar_frames/frame_12.png"),
                resource_path("assets/images/radar_frames/frame_13.png"),
                resource_path("assets/images/radar_frames/frame_14.png"),
                resource_path("assets/images/radar_frames/frame_15.png"),
                resource_path("assets/images/radar_frames/frame_16.png"),
                resource_path("assets/images/radar_frames/frame_17.png"),
                resource_path("assets/images/radar_frames/frame_18.png"),
                resource_path("assets/images/radar_frames/frame_19.png"),
                   ]

pathImageTorpedo = [resource_path("assets/images/Torpedo_correct.png"),resource_path("assets/images/Torpedo_incorrect.png")]
