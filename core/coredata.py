from typing import Union

class CoreData:
    def __init__(self):
        self.data = {
            'cycles': 0,
            'running': True,
        }

    def get_data(self, data_id:str) -> Union[object, None]:
        return self.data[data_id]

    def set_data(self, data_id:str, data:object) -> None:
        self.data[data_id] = data