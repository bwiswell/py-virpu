from typing import Tuple

import pygame as pg
from pygame.event import Event

from .coredata import CoreData
from .graphics import Graphics
from .canvas import Canvas
from ..components.ioport import IOPort
from ..components.wire import Wire
from ..ui.ui import UI

MOVE_SPEED = 25

class Controller:
    '''
    A class to handle IO and manage user interactions.

    Attributes:
        core_data (CoreData): The current core state object
        graphics (Graphics): The current graphics object
        canvas (Canvas): The current canvas object
        ui (UI): The current UI object
    '''

    def __init__(self, 
                    core_data:CoreData, 
                    graphics:Graphics, 
                    canvas:Canvas, 
                    ui:UI
                ):
        '''
        Initialize the Controller object.

        Parameters:
            core_data: The current core state object
            graphics: The current graphics object
            canvas: The current canvas object
            ui: The current UI object
        '''
        self._core_data = core_data
        self._graphics = graphics
        self._canvas = canvas
        self._ui = ui

    def _screen_to_canvas(self, s_pos:Tuple[int, int]) -> Tuple[int, int]:
        '''Convert a screen position to a canvas position.'''
        view_x, view_y = self._core_data.view_pos
        cx = view_x + s_pos[0]
        cy = view_y + s_pos[1]
        return cx, cy

    def _handle_move(self, pressed) -> None:
        '''Handle movement around the canvas.'''
        dx = 0
        dy = 0
        speed_mult = MOVE_SPEED
        if pressed[pg.K_a]:
            dx = -1
        elif pressed[pg.K_d]:
            dx = 1
        if pressed[pg.K_w]:
            dy = -1
        elif pressed[pg.K_s]:
            dy = 1
        if pressed[pg.K_LSHIFT]:
            speed_mult *= 2
        screen_size = self._core_data.screen_size
        view_pos = self._core_data.view_pos
        new_x = view_pos[0] + dx * speed_mult
        new_x = max(0, min(self._core_data.canvas_size[0] - screen_size[0], new_x))
        new_y = view_pos[1] + dy * speed_mult
        new_y = max(0, min(self._core_data.canvas_size[1] - screen_size[1], new_y))
        self._core_data.view_pos = new_x, new_y

    def _handle_held_keys(self) -> None:
        '''Handle any keys being pressed and held down.'''
        pressed = pg.key.get_pressed()
        self._handle_move(pressed)
        if pressed[pg.K_f]:
            self._canvas.tick()

    def _delete_placing(self) -> None:
        '''Delete the component currently being placed.'''
        placing = self._core_data.placing
        self._core_data.placing = None
        self._canvas.remove_wires(placing)

    def _handle_mousedown(self, event:Event) -> None:
        '''Handle a mouse click event.'''
        ui_target = self._ui.at_pos(event.pos)
        canvas_target = self._canvas.at_pos(event.pos)
        placing = self._core_data.placing
        wire = self._core_data.wire

        if ui_target is not None:
            self._delete_placing()
            self._core_data.wire = None
            ui_target.handle_click(event)

        elif canvas_target is not None and isinstance(canvas_target, IOPort):
            self._delete_placing()
            if event.button == 1:
                if canvas_target.dir == 'out':
                    self._core_data.wire = Wire(canvas_target)
                else:
                    wire = self._core_data.wire
                    self._core_data.wire = None
                    if wire is not None and wire.compatible(canvas_target):
                        wire.wire_out = canvas_target
                        self._canvas.add_wire(wire)
            else:
                self._core_data.wire = None
                self._canvas.remove_wires_from_port(canvas_target)

        elif canvas_target is not None:
            self._delete_placing()
            self._core_data.wire = None
            if event.button == 3:
                self._canvas.remove_component(canvas_target)
                self._core_data.placing = canvas_target

        elif placing is not None and event.button == 1:
            self._core_data.placing = None
            placing.center_on(event.pos)
            self._canvas.add_component(placing)

        elif placing is not None:
            self._delete_placing()

        elif wire is not None and event.button == 1:
            wire.add_waypoint(event.pos)

        elif wire is not None:
            self._core_data.wire = None

    def _handle_keydown(self, event:Event) -> None:
        '''Handle a key press event.'''
        if event.key == pg.K_ESCAPE:
            self._core_data.running = False
        elif event.key == pg.K_SPACE:
            self._canvas.tick()
        elif event.key == pg.K_DELETE:
            self._delete_placing()

    def _handle_hover(self) -> None:
        '''Check for and handle any panels currently being hovered.'''
        mouse_pos = pg.mouse.get_pos()
        ui_target = self._ui.at_pos(mouse_pos)
        if ui_target is not None:
            ui_target.handle_hover(mouse_pos)
        else:
            canv_pos = self._screen_to_canvas(mouse_pos)
            canvas_target = self._canvas.at_pos(canv_pos)
            if canvas_target is not None:
                canvas_target.handle_hover(canv_pos)

    def _render_overlay(self) -> None:
        '''Render any overlay graphics.'''
        buffer = self._graphics.overlay_buffer
        theme = self._core_data.overlay_theme
        mouse_pos = pg.mouse.get_pos()
        placing = self._core_data.placing
        if placing is not None:
            placing.center_on(mouse_pos)
            placing.render(buffer, theme)
        wire = self._core_data.wire
        if wire is not None:
            wire.render(buffer, theme, mouse_pos)

    def io_tick(self) -> None:
        '''Check for and handle user inputs and render overlay.'''
        self._handle_held_keys()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                self._handle_mousedown(event)
            elif event.type == pg.KEYDOWN:
                self._handle_keydown(event)
        self._handle_hover()
        self._render_overlay()