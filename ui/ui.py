from typing import List, Tuple

from ..core.coredata import CoreData
from ..core.graphics import Graphics
from ..panels.configuration import Configuration
from ..panels.panel import Panel

class UI:

    COLS = 8
    ROWS = 6

    def __init__(self, core_data:CoreData, graphics:Graphics):
        self.core_data = core_data
        self.graphics = graphics

        self.size = self.core_data.get_data('screen-size')
        self.grid_x_scale = self.size[0] // UI.COLS
        self.grid_y_scale = self.size[1] // UI.ROWS
        self.widget_size = (self.grid_x_scale // 2, self.grid_y_scale // 2)
        self.widget_x_off = self.grid_x_scale // 4
        self.widget_y_off = self.grid_y_scale // 4

        self.panels = {}
        self.grid_positions = {}

    def widget_pos(self, grid_pos:Tuple[int, int]) -> Tuple[int, int]:
        grid_x = grid_pos[0] % UI.COLS
        grid_y = grid_pos[1] % UI.ROWS
        screen_x = grid_x * self.grid_x_scale + self.widget_x_off
        screen_y = grid_y * self.grid_y_scale + self.widget_y_off
        return screen_x, screen_y

    def resize(self) -> None:
        self.size = self.core_data.get_data('screen-size')
        self.grid_x_scale = self.size[0] // UI.COLS
        self.grid_y_scale = self.size[1] // UI.ROWS
        self.widget_size = (self.grid_x_scale // 2, self.grid_y_scale // 2)
        self.widget_x_off = self.grid_x_scale // 4
        self.widget_y_off = self.grid_y_scale // 4

        for panel_id, panel in self.panels.items():
            panel_grid_pos = self.grid_positions[panel_id]
            new_pos = self.widget_pos(panel_grid_pos)
            panel.repos_resize(new_pos, self.widget_size)

    def register_panel(self, 
                        panel_id:str, 
                        grid_pos:Tuple[int, int], 
                        panel:Panel
                    ) -> None:
        panel_pos = self.widget_pos(grid_pos)
        panel.repos_resize(panel_pos, self.widget_size)
        self.panels[panel_id] = panel
        self.grid_positions[panel_id] = grid_pos

    def unregister_panel(self, panel_id:str):
        self.panels.pop(panel_id, None)
        self.grid_positions.pop(panel_id, None)

    def at_pos(self, pos:Tuple[int, int]) -> Panel:
        for panel in self.panels.values():
            if panel.collides(pos):
                return panel

    def redraw(self) -> None:
        buffer = self.graphics.clear_ui_buffer()
        theme = self.core_data.get_data('ui-theme')
        for panel in self.panels.values():
            panel.render(buffer, theme)