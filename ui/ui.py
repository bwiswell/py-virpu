from math import floor
from typing import Tuple, Union

from ..panels.button import Button
from ..panels.panel import Panel
from ..core.coredata import CoreData
from ..core.graphics import Graphics

class UI:

    COLS = 16
    ROWS = 9

    def __init__(self, core_data:CoreData, graphics:Graphics):
        self.core_data = core_data
        self.graphics = graphics

        self.size = self.core_data.get_data('screen-size')
        self.grid_x_scale = floor(self.size[0] / UI.COLS)
        self.grid_y_scale = floor(self.size[1] / UI.ROWS)
        self.widget_size = (self.grid_x_scale // 2, self.grid_y_scale // 2)
        self.widget_x_off = self.grid_x_scale // 4
        self.widget_y_off = self.grid_y_scale // 4

        self.panels = {}
        self.buttons = {}
        self.grid_positions = {}

    def widget_pos(self, grid_pos:Tuple[int, int]) -> Tuple[int, int]:
        screen_x = grid_pos[0] * self.grid_x_scale + self.widget_x_off
        screen_y = grid_pos[1] * self.grid_y_scale + self.widget_y_off
        return screen_x, screen_y

    def resize(self) -> None:
        self.size = self.core_data.get_data('screen-size')
        self.grid_x_scale = floor(self.size[0] / UI.COLS)
        self.grid_y_scale = floor(self.size[1] / UI.ROWS)
        self.widget_size = (self.grid_x_scale // 2, self.grid_y_scale // 2)
        self.widget_x_off = self.grid_x_scale // 4
        self.widget_y_off = self.grid_y_scale // 4

        for panel_id, panel in self.panels.items():
            panel_grid_pos = self.grid_positions[panel_id]
            new_pos = self.widget_pos(panel_grid_pos)
            panel.repos_resize(new_pos, self.widget_size)

        for button_id, button in self.buttons.items():
            button_grid_pos = self.grid_positions[button_id]
            new_pos = self.widget_pos(button_grid_pos)
            button.repos_resize(new_pos, self.widget_size)

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

    def register_button(self,
                        button_id:str,
                        grid_pos:Tuple[int, int],
                        button:Button
                    ) -> None:
        button_pos = self.widget_pos(grid_pos)
        button.repos_resize(button_pos, self.widget_size)
        self.buttons[button_id] = button
        self.grid_positions[button_id] = grid_pos

    def unregister_button(self, button_id:str):
        self.buttons.pop(button_id, None)
        self.grid_positions.pop(button_id, None)

    def get_clicked(self, click_pos:Tuple[int, int]) -> Union[Button, None]:
        for button in self.buttons.values():
            if button.collides(click_pos):
                return button

    def redraw(self) -> None:
        buffer = self.graphics.clear_ui_buffer()
        theme = self.core_data.get_data('ui-theme')
        for panel in self.panels.values():
            panel.render(buffer, theme)
        for button in self.buttons.values():
            button.render(buffer, theme)