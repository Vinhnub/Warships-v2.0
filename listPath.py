from constants import *
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path).replace("\\","/")

listPathImageMenuScreen = [resource_path("assets/images/background/image_1.png"),
                           resource_path("assets/images/background/image_3.png"),
                           resource_path("assets/images/background/image_4.png"),
                           resource_path("assets/images/background/image_5.png"),
                           resource_path("assets/images/background/image_6.png"),
                            ]

listPathImageLogo = [resource_path("assets/images/logo/frame_1.png"),
                     resource_path("assets/images/logo/frame_2.png"),
                     resource_path("assets/images/logo/frame_3.png"),
                     resource_path("assets/images/logo/frame_4.png"),
                     resource_path("assets/images/logo/frame_5.png"),
                     resource_path("assets/images/logo/frame_6.png"),
                     resource_path("assets/images/logo/frame_7.png"),
                     resource_path("assets/images/logo/frame_8.png"),
                            ]

listPathImageBannerFindingScreen = [((365, 150), [resource_path("assets/images/banner/image_1.png")]),
                                     ]

listPathImageBannerCreateRoomScreen = [((505, 225), [resource_path("assets/images/banner/image_2.png")]),
                                     ] 

listPathImageBannerJoinRoomScreen = [((295, 225), [resource_path("assets/images/banner/image_3.png")]),
                                     ] 

listPathShipOnl = [(resource_path("assets/images/ship2.png"), (FIELD_COORD[0] + 3, FIELD_COORD[1] + 3), 1),
               (resource_path("assets/images/ship3.png"), (FIELD_COORD[0] + 3 + CELL_SIZE[0]*1, FIELD_COORD[1] + 3), 2),
               (resource_path("assets/images/ship3.png"), (FIELD_COORD[0] + 3 + CELL_SIZE[0]*2, FIELD_COORD[1] + 3), 3),
               (resource_path("assets/images/ship4.png"), (FIELD_COORD[0] + 3 + CELL_SIZE[0]*3, FIELD_COORD[1] + 3), 4),
               (resource_path("assets/images/ship5.png"), (FIELD_COORD[0] + 3 + CELL_SIZE[0]*4, FIELD_COORD[1] + 3), 5),
               (resource_path("assets/images/radar.png"), (FIELD_COORD[0] + 3 + CELL_SIZE[0]*5, FIELD_COORD[1] + 3), 6),
               (resource_path("assets/images/radar.png"), (FIELD_COORD[0] + 3 + CELL_SIZE[0]*6, FIELD_COORD[1] + 3), 7),
               ]
# id 6, 7 is radar

listPathShipOff = [(resource_path("assets/images/ship2.png"), (FIELD_COORD[0] + 3, FIELD_COORD[1] + 3), 1),
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

pathImageTorpedo = [resource_path("assets/images/Torpedo_correct.png"),resource_path("assets/images/Torpedo_incorrect.png"), resource_path("assets/images/Torpedo_radar.png")]
