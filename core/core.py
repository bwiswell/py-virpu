from typing import List

import pygame as pg

from .canvas import Canvas
from .controller import Controller
from .coredata import CoreData
from . import coreutils
from .graphics import Graphics
from ..corium import corium, translator
from ..ui.ui import UI

class Core:
    '''
    The main program object that manages the graphics, controller, and canvas/ui.

    Attributes:
        core_data (CoreData): The current core state object
        graphics (Graphics): The current graphics object
        canvas (Canvas): The current canvas object
        ui (UI): The current UI object
        controller (Controller): The current controller object
    '''

    def __init__(self, program:List[str]=None):
        '''
        Initialize the Core object and start the program.

        Parameters:
            program: An assembly program to load into memory (default None)
        '''
        corium.init()
        pg.init()
        self._core_data = CoreData()
        self._graphics = Graphics(self._core_data)
        self._canvas = Canvas(self._core_data, self._graphics)
        self._ui = UI(self._core_data, self._graphics)
        self._controller = Controller(self._core_data, 
                                        self._graphics, 
                                        self._canvas, 
                                        self._ui
                                    )
        
        coreutils.load_ui(self._core_data, self._ui)

        self._run()

    def _run(self) -> None:
        '''Main program loop.'''
        while self._core_data.running:
            self._controller.io_tick()
            self._canvas.redraw()
            self._ui.redraw()
            self._graphics.render()