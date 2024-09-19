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
    def __init__(self, filepath, key=-1, columns=1, rows=1):
        self.tex = TextureResource(filepath, False)
        self.width = self.tex.width
        self.height = self.tex.height
        self.data = self.tex.data
        self.key = key
        self.columns = columns
        self.rows = rows
        self.tileWidth = self.width // self.columns
        self.tileHeight = self.height // self.rows

class Sprite:
    def __init__(self, bitmap, x=0, y=0, frame=0, mirrorX=0, mirrorY=0):
        self.bitmap = bitmap
        self.x = x
        self.y = y
        self.frame = frame
        self.mirrorX = mirrorX
        self.mirrorY = mirrorY

class BitmapLayer:
    def __init__(self, bitmap=None, x=0, y=0, frame=0):
        self.bitmap = bitmap
        self.x = x
        self.y = y
        self.frame = frame
        
    @micropython.viper
    def render(buf:ptr16, offset:int, x:int, y:int, w:int):
        pass

class TileLayer:
    def __init__(self, columns, rows, bitmap=None, tilemap=None, x=0, y=0):
        self.columns = columns
        self.rows = rows
        self.bitmap = bitmap
        if tilemap is None:
            self.tilemap = bytearray(columns * rows)
        else:
            self.tilemap = tilemap
        self.x = 0
        self.y = 0
        
    @micropython.viper
    def render(buf:ptr16, offset:int, x:int, y:int, w:int):
        pass

class SpriteLayer:
    def __init__(self):
        self.sprites = []
        
    @micropython.viper
    def render(buf:ptr16, offset:int, x:int, y:int, w:int):
        pass
        

# class ScanLine:
#     def __init__(self):
#         self.pixels = array.array("H",[Color.BLACK for _ in range(WIDTH)])
#         self.commands = []

class PPU:
    buf = engine_io.back_fb_data()
    
    layers = []
    # scanLines = [ScanLine() for _ in range(HEIGHT)]
    scanStarted = False
    cx, cy = 0, 0

    @micropython.native
    def ScanLine(y:int):
        cy = PPU.cy
        offset = cy * WIDTH
        buf = PPU.buf
        while cy < y:
            for layer in PPU.layers:
                layer.render(buf, offset, 0, cy, WIDTH)
            cy += 1
            offset += WIDTH
        PPU.cy = cy

    @micropython.native
    def ScanX(x:int):
        cx = PPU.cx
        cy = PPU.cy
        buf = PPU.buf
        offset = cy * WIDTH + cx
        w = x - cx
        for layer in PPU.layers:
            layer.render(buf, offset, cx, cy, w)
        PPU.cx = cx + w
    
    @micropython.native
    def ScanXEnd():
        cx = PPU.cx
        cy = PPU.cy
        buf = PPU.buf
        offset = cy * WIDTH + cx
        w = WIDTH - cx
        if w > 0:
            for layer in PPU.layers:
                layer.render(buf, offset, cx, cy, w)
        PPU.cx = 0
        PPU.cy += 1

    @micropython.native
    def Update():
        while not engine.tick():
            pass
        
    def setFPS(fps):
        engine.fps_limit(fps)