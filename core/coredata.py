from typing import Union

from ..ui.theme import Theme

class CoreData:
    def __init__(self):
        self.data = {
            'cycles': 0,
            'running': True,
            'canvas-theme': Theme(
                bg_color=(0, 0, 0),
                border_color=(255, 255, 255),
                border_width=2,
                text_color=(255, 255, 255)
            ),
            'ui-theme': Theme(
                bg_color=(255, 255, 255),
                border_color=(0, 0, 0),
                border_width = 2,
            )
        }

    def get_data(self, data_id:str) -> Union[object, None]:
        return self.data[data_id]

    def set_data(self, data_id:str, data:object) -> None:
        self.data[data_id] = data