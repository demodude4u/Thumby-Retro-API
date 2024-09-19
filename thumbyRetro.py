import engine_main

import engine
import engine_io
import engine_draw

from engine_resources import TextureResource

import array

WIDTH = const(128)
HEIGHT = const(128)

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

class Color:
    BLACK = const(0x0000)
    NAVY = const(0x000F)
    DARKGREEN = const(0x03E0)
    DARKCYAN = const(0x03EF)
    MAROON = const(0x7800)
    PURPLE = const(0x780F)
    OLIVE = const(0x7BE0)
    LIGHTGREY = const(0xD69A)
    DARKGREY = const(0x7BEF)
    BLUE = const(0x001F)
    GREEN = const(0x07E0)
    CYAN = const(0x07FF)
    RED = const(0xF800)
    MAGENTA = const(0xF81F)
    YELLOW = const(0xFFE0)
    WHITE = const(0xFFFF)
    ORANGE = const(0xFDA0)
    GREENYELLOW = const(0xB7E0)
    PINK = const(0xFE19)
    BROWN = const(0x9A60)
    GOLD = const(0xFEA0)
    SILVER = const(0xC618)
    SKYBLUE = const(0x867D)
    VIOLET = const(0x915C)

class Bitmap:
    @micropython.native
    def __init__(self, filepath, key=-1):
        self.tex = TextureResource(filepath, False)
        self.width = self.tex.width
        self.height = self.tex.height
        self.data = self.tex.data
        self.key = key

class Tileset:
    @micropython.native
    def __init__(self, filepath, columns, rows, key=-1):
        self.tex = TextureResource(filepath, False)
        self.width = self.tex.width
        self.height = self.tex.height
        self.data = self.tex.data
        self.columns = columns
        self.rows = rows
        self.key = key

        self.tileWidth = self.width // self.columns
        self.tileHeight = self.height // self.rows

class Sprite:
    pass

class BitmapLayer:
    def __init__(self):
        self.bitmap = None
        self.x = 0
        self.y = 0

class TileLayer:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.data = bytearray(columns * rows)

        self.tileset = None
        self.x = 0
        self.y = 0

class SpriteLayer:
    def __init__(self):
        self.sprites = []

class ScanLine:
    def __init__(self):
        self.pixels = array.array("H",[Color.BLACK for _ in range(WIDTH)])
        self.commands = []

class PPU:
    layers = []
    scanLines = [ScanLine() for _ in range(HEIGHT)]

    def StartLine():
        pass

    def JumpLine(y:int):
        pass

    def JumpLinePixel(x:int):
        pass

    def NextLine(count:int=1):
        pass

    def Update():
        pass