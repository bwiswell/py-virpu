from .coredata import CoreData
from .graphics import Graphics

class Core:
    def __init__(self):
        self.core_data = CoreData()
        self.graphics = Graphics(self.core_data)
        # TODO: Create canvas object
        # TODO: Create ui object
        # TODO: Create controller object
        pass

    def run(self) -> None:
        # TODO: Implement run function
        # While the 'running' flag in the core data is True:
            # Check IO
            # Re-render canvas
            # Re-render ui
            # Re-render screen as composite of canvas and ui
        pass