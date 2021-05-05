from typing import Union

from ..ui.theme import Theme

class CoreData:
    '''
    A class to store session information.
    
    Attributes:
        running (bool): Main flag for continuing/exiting program
        ticks (int): The number of clock cycles so far
        screen_size (Tuple[int, int]): The size of the display screen
        placing (Component): The component currently being placed
        wire (Wire): The wire currently being placed
        canvas_theme (Theme): The theme to use when rendering the canvas
        ui_theme (Theme): The theme to use when rendering the UI
        overlay_theme (Theme): The theme to use when rendering the overlay
    '''
    def __init__(self):
        '''Initialize CoreData object.'''
        self.running = True
        self.ticks = 0

        self.screen_size = (0, 0)

        self.placing = None
        self.wire = None

        self.canvas_theme = Theme(
                                    bg_col=(0, 0, 0),
                                    act_col=(0, 0, 0),
                                    wire_col=(255, 255, 255),
                                    txt_col=(255, 255, 255),
                                    bord_col=(255, 255, 255)
                                )
        self.ui_theme = Theme(
                                bg_col=(255, 255, 255),
                                act_col=(191, 191, 191),
                                wire_col=(95, 31, 31),
                                txt_col=(0, 0, 0),
                                bord_col=(0, 0, 0)
                            )
        self.overlay_theme = Theme(
                                    bg_col=(255, 255, 255),
                                    act_col=(191, 191, 191),
                                    wire_col=(95, 31, 31),
                                    txt_col=(0, 0, 0),
                                    bord_col=(0, 0, 0)
                                )