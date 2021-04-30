import pygame as pg

from .canvas import Canvas
from .coredata import CoreData
from .graphics import Graphics
from ..ui.ui import UI

class Core:
    def __init__(self):
        pg.init()
        self.core_data = CoreData()
        self.graphics = Graphics(self.core_data)
        self.canvas = Canvas(self.core_data, self.graphics)
        self.ui = UI(self.core_data, self.graphics)
        # TODO: Create controller object
        self.run()

    def run(self) -> None:
        while self.core_data.get_data('running'):
            self.canvas.redraw()
            self.ui.redraw()
            self.graphics.render()