import engine_main

import engine
import engine_io
import engine_draw

from engine_resources import TextureResource

import array

WIDTH = const(128)
"""Width of the screen, in pixels."""
HEIGHT = const(128)
"""Height of the screen, in pixels."""

# Button Aliasing (same as engine_io buttons)
BtnA = engine_io.A
BtnB = engine_io.B
BtnU = engine_io.UP
BtnD = engine_io.DOWN
BtnL = engine_io.LEFT
BtnR = engine_io.RIGHT
BtnLB = engine_io.LB
BtnRB = engine_io.RB
BtnMENU = engine_io.MENU

class Bitmap:
    pass

class Tilemap:
    pass

class Sprite:
    pass

class _BitmapLayer:
    pass

class _TileLayer:
    pass

class _SpriteLayer:
    pass

class _ScanLine:
    def __init__(self):
        self.pixels = array.array("H",[0x0000 for _ in range(WIDTH)])
        self.dirty = True

_layers = []
_scanLines = [_ScanLine() for _ in range(HEIGHT)]
class PPU:
    pass