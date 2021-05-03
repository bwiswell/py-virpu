from typing import Union

from ..ui.theme import Theme

class CoreData:
    def __init__(self):
        self.data = {
            'ticks': 0,
            'running': True,
            'placing': None,
            'comp-config': None,
            'canvas-theme': Theme(
                bg_color=(0, 0, 0),
                active_color=(0, 0, 0),
                border_color=(255, 255, 255),
                border_width=2,
                text_color=(255, 255, 255)
            ),
            'ui-theme': Theme(
                bg_color=(255, 255, 255),
                active_color=(191, 191, 191),
                border_color=(0, 0, 0),
                border_width = 2,
            ),
            'overlay-theme': Theme(
                bg_color=(255, 255, 255),
                active_color=(191, 191, 191),
                border_color=(127, 31, 31),
                border_width = 2,
            ),
            'wire': None
        }

    def get_data(self, data_id:str) -> Union[object, None]:
        return self.data[data_id]

    def set_data(self, data_id:str, data:object) -> None:
        self.data[data_id] = data