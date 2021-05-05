from typing import List, Tuple

from ..core.coredata import CoreData
from ..core.graphics import Graphics
from ..panels.panel import Panel

class UI:
    '''
    A class to manage the UI and its comprising panels.

    Attributes:
        core_data (CoreData): The current core state object
        graphics (Graphics): The current graphics object
        gx_scale (int): Scaling factor between grid x- and screen x-coordinates
        gy_scale (int): Scaling factor between grid y- and screen y-coordinates
        panel_size (Tuple[int, int]): The current size of a UI panel
        panel_x_off (int): The grid-cell x-offset of a UI panel
        panel_y_off (int): The grid-cell y-offset of a UI panel
        panels (Dict[str, Panel]): UI panels indexed by panel ID
        panel_positions (Dict[str, Tuple[int, int]]): Current UI panel positions
    '''

    COLS = 8
    ROWS = 6

    def __init__(self, core_data:CoreData, graphics:Graphics):
        '''
        Initialize the UI object.

        Parameters:
            core_data: The current core state object
            graphics: The current graphics object
        '''
        self._core_data = core_data
        self._graphics = graphics

        self._gx_scale = 0
        self._gy_scale = 0
        self._panel_size = (0, 0)
        self._panel_x_off = 0
        self._panel_y_off = 0

        self._panels = {}
        self._panel_positions = {}

        self.resize()

    def grid_to_screen(self, grid_pos:Tuple[int, int]) -> Tuple[int, int]:
        '''Convert a UI grid position to a screen position.'''
        gx = grid_pos[0] % UI.COLS
        gy = grid_pos[1] % UI.ROWS
        screen_x = gx * self._gx_scale + self._panel_x_off
        screen_y = gy * self._gy_scale + self._panel_y_off
        return screen_x, screen_y

    @property
    def size(self) -> Tuple[int, int]:
        '''Get the UI size.'''
        return self._core_data.screen_size

    def resize(self) -> None:
        '''Resize the UI after the screen size changes.'''
        self._gx_scale = self.size[0] // UI.COLS
        self._gy_scale = self.size[1] // UI.ROWS
        self._panel_size = (self._gx_scale // 2, self._gy_scale // 2)
        self._panel_x_off = self._gx_scale // 4
        self._panel_y_off = self._gy_scale // 4

        for panel_id, panel in self._panels.items():
            panel.size = self._panel_size
            panel_grid_pos = self._panel_positions[panel_id]
            panel.pos = self.grid_to_screen(panel_grid_pos)

    def register_panel(self, 
                        panel_id:str, 
                        grid_pos:Tuple[int, int], 
                        panel:Panel
                    ) -> None:
        '''
        Add a panel to the UI.

        Parameters:
            panel_id: the id of the panel to add
            grid_pos: the position of the panel to add
            panel: the panel to add
        '''
        panel.size = self._panel_size
        panel.pos = self.grid_to_screen(grid_pos)
        self._panels[panel_id] = panel
        self._panel_positions[panel_id] = grid_pos

    def unregister_panel(self, panel_id:str):
        '''
        Remove a panel from the UI.

        Parameters:
            panel_id: the id of the panel to remove
        '''
        self.panels.pop(panel_id, None)
        self.grid_positions.pop(panel_id, None)

    def at_pos(self, pos:Tuple[int, int]) -> Panel:
        '''Detect and return the panel at the given position.'''
        for panel in self._panels.values():
            if panel.collides(pos):
                return panel

    def redraw(self) -> None:
        '''Redraw the UI and UI panels to the UI buffer.'''
        buffer = self._graphics.ui_buffer
        theme = self._core_data.ui_theme
        for panel in self._panels.values():
            panel.render(buffer, theme)