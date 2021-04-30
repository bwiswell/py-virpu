import pygame as pg

from .coredata import CoreData

class Graphics:
    def __init__(self, core_data:CoreData):
        self.core_data = core_data

        self.screen = pg.display.set_mode(flags=pg.FULLSCREEN)
        screen_w, screen_h = screen_size = self.screen.get_size()
        self.core_data.set_data('fullscreen', True)
        self.core_data.set_data('screen-w', screen_w)
        self.core_data.set_data('screen-h', screen_h)
        self.core_data.set_data('screen-size', screen_size)

        self.canvas_buffer = pg.Surface(screen_size)
        self.ui_buffer = pg.Surface(screen_size, pg.SRCALPHA)
        self.overlay_buffer = pg.Surface(screen_size, pg.SRCALPHA)

    def get_canvas_buffer(self) -> pg.Surface:
        return self.canvas_buffer

    def get_ui_buffer(self) -> pg.Surface:
        return self.ui_buffer

    def get_overlay_buffer(self) -> pg.Surface:
        return self.overlay_buffer

    def clear_canvas_buffer(self) -> pg.Surface:
        self.canvas_buffer.fill((0, 0, 0))
        return self.canvas_buffer

    def clear_ui_buffer(self) -> pg.Surface:
        self.ui_buffer.fill(pg.SRCALPHA)
        return self.ui_buffer

    def clear_overlay_buffer(self) -> pg.Surface:
        self.overlay_buffer.fill(pg.SRCALPHA)
        return self.overlay_buffer

    def render(self) -> None:
        self.screen.blit(self.canvas_buffer, (0, 0))
        self.screen.blit(self.ui_buffer, (0, 0))
        self.screen.blit(self.overlay_buffer, (0, 0))
        pg.display.update()