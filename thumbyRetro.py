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
    def __init__(self, bitmap, x=0, y=0, frame=0):
        self.bitmap = bitmap
        self.x = x
        self.y = y
        self.width = bitmap.tileWidth
        self.height = bitmap.tileHeight
        self.frame = frame
        # TODO
        # self.mirrorX = mirrorX
        # self.mirrorY = mirrorY

class BitmapLayer:
    def __init__(self, bitmap=None, x=0, y=0, frame=0):
        self.bitmap = bitmap
        self.x = x
        self.y = y
        self.frame = frame

    @micropython.viper
    def start(self):
        pass
        
    @micropython.viper
    def render(self, buf:ptr16, offset:int, x:int, y:int, w:int):
        bitmap = self.bitmap
        bmp = ptr16(bitmap.data)
        srcW = int(bitmap.tileWidth)
        srcH = int(bitmap.tileHeight)
        cols = int(bitmap.columns)
        bmpW = int(bitmap.width)
        key = int(bitmap.key) 
        frame = int(self.frame)

        srcY = ((((y-int(self.y)) % srcH) + srcH) % srcH)
        if frame > 0:
            row = frame // cols
            col = frame % cols
            srcX = col * srcW
            srcY += row * srcH
        else:
            srcX = 0
        si1 = srcY * bmpW + srcX
        si = si1 + ((((x-int(self.x)) % srcW) + srcW) % srcW)
        di = offset
        for _ in range(w):
            if (si-si1) == srcW:
                si = si1
            c = bmp[si] & 0xFFFF
            if c != key:
                buf[di] = c
            si += 1
            di += 1

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
    def start(self):
        pass # TODO

    @micropython.viper
    def render(self, buf:ptr16, offset:int, x:int, y:int, w:int):
        pass # TODO

_SL_CACHE_COUNT = const(0)
_SL_CACHE_YSTOP = const(1)
_SL_CACHE_MINSIZE = const(16)

class SpriteLayer:
    def __init__(self):
        self.sprites = []

        self._cache = bytearray(_SL_CACHE_MINSIZE)
        self._cacheMeta = array.array("h",[0,-1])
        
    @micropython.viper
    def invalidate(self):
        cacheMeta = ptr16(self._cacheMeta)
        cacheMeta[_SL_CACHE_YSTOP] = -1

    @micropython.viper
    def start(self):
        cacheMeta = ptr16(self._cacheMeta)
        cacheMeta[_SL_CACHE_YSTOP] = -1

    @micropython.viper
    def render(self, buf:ptr16, offset:int, x:int, y:int, w:int):
        cache = ptr8(self._cache)
        cacheMeta = self._cacheMeta
        cacheMetaWrite = ptr16(self._cacheMeta)
        
        sprites = self.sprites
        # print(x,y,w,"-- CHECK",cacheMeta[_SL_CACHE_COUNT],cacheMeta[_SL_CACHE_YSTOP])
        if y > int(cacheMeta[_SL_CACHE_YSTOP]):
            # print("???",y,int(cacheMeta[_SL_CACHE_YSTOP]))
            minY2 = HEIGHT-1
            nextY1 = HEIGHT-1
            ci = 0
            for i in range(int(len(sprites))):
                sprite = sprites[i]
                y1 = int(sprite.y)
                y2 = y1 + int(sprite.height)
                if y < y1:
                    nextY1 = int(min(nextY1, y1))
                    if y >= y2:
                        # print("-----",y,"-",i,y1,y2,"SKIP")
                        continue
                minY2 = int(min(minY2, y2))
                cache[ci] = i
                ci += 1
                # print("-----",y,"-",i,y1,y2,"ADD")
            count = ci
            cacheMetaWrite[_SL_CACHE_COUNT] = count
            if count > 0:
                cacheMetaWrite[_SL_CACHE_YSTOP] = minY2 - 1
            else:
                cacheMetaWrite[_SL_CACHE_YSTOP] = nextY1 - 1
            # print(x,y,w,"-- CACHE",cacheMeta[_SL_CACHE_COUNT],cacheMeta[_SL_CACHE_YSTOP])
        else:
            count = int(cacheMeta[_SL_CACHE_COUNT])

        buf = ptr16(PPU.buf)
        for ci in range(count):
            sprite = sprites[cache[ci]]
            sprW = int(sprite.width)
            sprH = int(sprite.height)
            bitmap = sprite.bitmap
            cols = int(bitmap.columns)
            bmpW = int(bitmap.width)
            bmp = ptr16(bitmap.data)
            key = int(bitmap.key) 
            frame = int(sprite.frame)

            srcY = y - int(sprite.y)
            if frame > 0:
                row = frame // cols
                col = frame % cols
                srcX = col * sprW
                srcY += row * sprH
            else:
                srcX = 0

            dstX = int(sprite.x)
            
            if dstX < x:
                d = (x-dstX)
                srcX += d
                sprW -= d
                dstX = x
            dx2 = dstX + sprW
            x2 = x + w
            if dx2 >= x2:
                sprW -= dx2 - x2

            # print(x, y, w, "|", srcX, srcY, sprW, "|", dstX)

            si = srcY * bmpW + srcX
            di = y * WIDTH + dstX
            for _ in range(sprW):
                c = bmp[si] & 0xFFFF
                if c != key:
                    buf[di] = c
                si += 1
                di += 1

        
# TODO deferred rendering techniques?
# class ScanLine:
#     def __init__(self):
#         self.pixels = array.array("H",[Color.BLACK for _ in range(WIDTH)])
#         self.commands = []

class PPU:
    buf = engine_draw.back_fb_data()
    
    layers = []
    # scanLines = [ScanLine() for _ in range(HEIGHT)]
    scanStarted = False
    cx, cy = 0, 0

    @micropython.native
    def scanStart():
        for layer in PPU.layers:
            layer.start()

    @micropython.native
    def scanLine(y:int):
        cy = PPU.cy
        offset = cy * WIDTH
        buf = PPU.buf
        while cy <= y:
            for layer in PPU.layers:
                layer.render(buf, offset, 0, cy, WIDTH)
            cy += 1
            offset += WIDTH
        PPU.cy = cy

    @micropython.native
    def scanX(x:int):
        cx = PPU.cx
        cy = PPU.cy
        buf = PPU.buf
        offset = cy * WIDTH + cx
        w = x - cx
        for layer in PPU.layers:
            layer.render(buf, offset, cx, cy, w)
        PPU.cx = cx + w
    
    @micropython.native
    def scanXEnd():
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
    def update():
        cy = PPU.cy
        offset = cy * WIDTH
        buf = PPU.buf
        while cy < HEIGHT:
            for layer in PPU.layers:
                layer.render(buf, offset, 0, cy, WIDTH)
            cy += 1
            offset += WIDTH
        PPU.cx = 0
        PPU.cy = 0
        while not engine.tick():
            pass
        
    def setFPS(fps):
        engine.fps_limit(fps)