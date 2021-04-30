import pygame as pg

from .coredata import CoreData

class Graphics:
    def __init__(self, core_data:CoreData):
        self.core_data = core_data
        pg.init()

        self.screen = pg.display.set_mode(flags=pg.FULLSCREEN)
        screen_w, screen_h = self.screen.get_size()
        self.core_data.set_data('fullscreen', True)
        self.core_data.set_data('screen-w', screen_w)
        self.core_data.set_data('screen-h', screen_h)

        self.canvas_buffer = pg.Surface((screen_w, screen_h))
        self.ui_buffer = pg.Surface((screen_w, screen_h), pg.SRCALPHA)
        self.overlay_buffer = pg.Surface((screen_w, screen_h), pg.SRCALPHA)

    def get_canvas_buffer(self) -> pg.Surface:
        return self.canvas_buffer

    def get_ui_buffer(self) -> pg.Surface:
        return self.ui_buffer

    def get_overlay_buffer(self) -> pg.Surface:
        return self.overlay_buffer

    def clear_canvas_buffer(self) -> None:
        self.canvas_buffer.fill((0, 0, 0))

    def clear_ui_buffer(self) -> None:
        self.ui_buffer.fill(pg.SRCALPHA)

    def clear_overlay_buffer(self) -> None:
        self.overlay_buffer.fill(pg.SRCALPHA)

    def render(self) -> None:
        self.screen.blit(self.canvas_buffer, (0, 0))
        self.screen.blit(self.ui_buffer, (0, 0))
        self.screen.blit(self.overlay_buffer, (0, 0))
        pg.display.update()