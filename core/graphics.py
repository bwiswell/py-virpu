from typing import Tuple

from pygame import display, Rect, Surface, FULLSCREEN, SRCALPHA
import pygame

from .coredata import CoreData

class Graphics:
    '''
    A class to store and manage rendering buffers.

    Attributes:
        core_data (CoreData): The current core state object
        screen (Surface): The output display surface
        canvas_buffer (Surface): The canvas' render buffer
        ui_buffer (Surface): The UI's render buffer
        overlay_buffer (Surface): The overlay's render buffer
    '''
    def __init__(self, core_data:CoreData, start_screen:bool=True):
        '''
        Initialize the Graphics object.

        Parameters:
            core_data: The current core state object
        '''
        self._core_data = core_data

        if start_screen:
            self._screen = display.set_mode(flags=FULLSCREEN)
        else:
            self._screen = Surface((1, 1))
        self._core_data.screen_size = self._screen.get_size()

        self._canvas_buffer = Surface(self._core_data.canvas_size)
        self._ui_buffer = Surface(self.size, SRCALPHA)
        self._overlay_buffer = Surface(self.size, SRCALPHA)

    @property
    def size(self) -> Tuple[int, int]:
        '''Get the graphics size.'''
        return self._core_data.screen_size

    @property
    def canvas_buffer(self) -> Surface:
        '''Get the canvas graphics buffer.'''
        self._canvas_buffer.fill((0, 0, 0))
        return self._canvas_buffer

    @property
    def ui_buffer(self) -> Surface:
        '''Get the UI graphics buffer.'''
        self._ui_buffer.fill(SRCALPHA)
        return self._ui_buffer

    @property
    def overlay_buffer(self) -> Surface:
        '''Get the overlay graphics buffer.'''
        self._overlay_buffer.fill(SRCALPHA)
        return self._overlay_buffer

    def render(self) -> None:
        '''Render the canvas, UI, and overlay buffers to the display.'''
        view_rect = Rect(self._core_data.view_pos, self._core_data.screen_size)
        self._screen.blit(self._canvas_buffer, (0, 0), view_rect)
        self._screen.blit(self._ui_buffer, (0, 0))
        self._screen.blit(self._overlay_buffer, (0, 0))
        display.update()