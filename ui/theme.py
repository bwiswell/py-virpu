from typing import Tuple

from pygame import Surface
from pygame.font import Font, SysFont

class Theme:
    '''
    A class to track custom color and layout schemes to use for rendering.

    Parameters:
        bg_col (Tuple[int, int, int]): The background color
        act_col (Tuple[int, int, int]): The color of 'active' objects
        txt_col (Tuple[int, int, int]): The text color
        bord_col (Tuple[int, int, int]): The border color
        bord_w (int): The border width
        bord_r (int): The border radius
        sm_font (Font): The small-sized font
        md_font (Font): The medium-sized font
        lg_font (Font): The large-sized font
    '''
    def __init__(self,
                    bg_col:Tuple[int, int, int],
                    act_col:Tuple[int, int, int],
                    wire_col:Tuple[int, int, int],
                    txt_col:Tuple[int, int, int],
                    bord_col:Tuple[int, int, int],
                    bord_w:int=2,
                    bord_r:int=10,
                    font_name:str=None,
                    sm_font_size:int=12,
                    md_font_size:int=18,
                    lg_font_size:int=24
                ):
        '''
        Initialize the Theme object and its fonts.

        Parameters:
            bg_col: The background color
            act_col: The color of 'active' objects
            wire_col: The wire color
            txt_col: The text color
            bord_col: The border color
            bord_w: The border width (default 10)
            bord_r: The border radius (default 10)
            font_name: The name of the font to use (default None)
            sm_font_size: The small font size (default 12)
            md_font_size: The medium font size (default 18)
            lg_font_size: The large font size (default 24)
        '''
        self.bg_col = bg_col
        self.act_col = act_col
        self.wire_col = wire_col
        self.txt_col = txt_col
        self.bord_col = bord_col
        self.bord_w = bord_w
        self.bord_r = bord_r
        self._sm_font = SysFont(font_name, sm_font_size)
        self._md_font = SysFont(font_name, md_font_size)
        self._lg_font = SysFont(font_name, lg_font_size)

    def _render_text(self, text_obj:object, font:Font) -> Surface:
        '''Render a text version of text_obj using the given font.'''
        return font.render(str(text_obj), True, self.txt_col)

    def small_text(self, text_obj:object) -> Surface:
        '''Render a text version of text_obj using the small font.'''
        return self._render_text(text_obj, self._sm_font)

    def medium_text(self, text_obj:object) -> Surface:
        '''Render a text version of text_obj using the medium font.'''
        return self._render_text(text_obj, self._md_font)
        
    def large_text(self, text_obj:object) -> Surface:
        '''Render a text version of text_obj using the large font.'''
        return self._render_text(text_obj, self._lg_font)