
### IDEAS
# Screen effects
#   - Shaking
#   - Scene transition
#   - Spotlight
#   - Page turn
# Sprite distortions
#   - Stretching
#   - Bending
#   - Squish/Bounce
# Animations
#   - Water Waves
#   - Windy Grass
# Transformations
#   - Deforming
#   - "Mode 7"
###


from thumbyRetro import *

import math
import array

bmpTile = Bitmap("tile.bmp")

bmpCastle = Bitmap("castle.bmp", Color.MAGENTA)
bmpCastleBG = Bitmap("castle_bg.bmp")

bmpRiverEdge = Bitmap("river_edge.bmp", Color.MAGENTA)
bmpRiverBed = Bitmap("river_bed.bmp", Color.MAGENTA)
bmpRiverFlow = Bitmap("river_flow.bmp", Color.MAGENTA)
bmpGrass = Bitmap("grass.bmp")

bmpPainting = Bitmap("painting.bmp")
bmpPaintingMask = Bitmap("painting_mask.bmp", Color.MAGENTA)

#
#   Castle
#
def test_castle():
    layerSky = BitmapLayer(bmpCastleBG)
    layerBG = BitmapLayer(bmpCastle)
    PPU.layers = [
        layerSky,
        layerBG
    ]

    skyX = 0
    bgX = 0
    t = 0
    intensity = 2
    while True:
        # Next test
        dTest = 1 if BtnRB.is_just_pressed else -1 if BtnLB.is_just_pressed else 0
        if dTest:
            return dTest

        dx = 1 if BtnR.is_pressed else -1 if BtnL.is_pressed else 0
        dint = 0.1 if BtnU.is_pressed else -0.1 if BtnD.is_pressed else 0
        
        bgX = max(0,min(layerBG.bitmap.width-WIDTH,bgX+dx))
        intensity = max(0,min(5,intensity+dint))
                    
        layerBG.x = -bgX
        skyX -= 0.25 * intensity
        t += 0.01 * intensity
        r = 5 * intensity
        PPU.scanStart()
        for y in range(HEIGHT):
            layerSky.x = int(skyX-bgX+r*math.sin(t+y/10))
            PPU.scanLine(y)
        PPU.update()

#
#   River
#
def test_river():
    layerGrass = BitmapLayer(bmpGrass)
    layerRiver = SpriteLayer()
    PPU.layers = [
        layerGrass,
        layerRiver
    ]

    sprEdge = Sprite(bmpRiverEdge)
    sprBed = Sprite(bmpRiverBed)
    sprFlow = Sprite(bmpRiverFlow)
    sprFlow2 = Sprite(bmpRiverFlow)
    layerRiver.sprites = [
        sprEdge,
        sprBed,
        sprFlow,
        sprFlow2,
    ]
    
    frame = 0
    curve = 16
    while True:
        # Next test
        dTest = 1 if BtnRB.is_just_pressed else -1 if BtnLB.is_just_pressed else 0
        if dTest:
            return dTest

        dCurve = 0.5 if BtnR.is_pressed else -0.5 if BtnL.is_pressed else 0

        curve = max(0,min(32,curve+dCurve))

        frame += 1
        
        PPU.scanStart()
        sprEdge.y = 0
        sprBed.y = 0
        sprFlow.y = ((frame//2) % sprFlow.height) - sprFlow.height
        sprFlow2.y = (frame % sprFlow.height) - sprFlow.height
        for y in range(HEIGHT):
            x = int(64 + curve * math.sin(y/20))
            changed = False
            for sprite in layerRiver.sprites: # Sprite Multiplexing
                sprite.x = x - sprite.width//2
                if y >= sprite.y + sprite.height:
                    sprite.y += sprite.height
                    changed = True
            sprFlow.x += int(2*math.sin(frame/50+y/10))
            sprFlow2.x += int(2*math.sin(frame/70+y/10))
            if changed:
                layerRiver.invalidate()
            PPU.scanLine(y)
        PPU.update()

#
#   Shockwave
#
def test_shockwave():
    # animSequence = array.array("b",[int(5*((3-x)/3)*math.sin((3-x)*(3-x))) for x in range(0,3,1/30)])
    # TODO maybe don't need LUT at first
    # return 1 # TODO
    
    layerWater = BitmapLayer(bmpPainting)
    layerMask = BitmapLayer(bmpPaintingMask)
    PPU.layers = [
        layerWater,
        layerMask,
    ]

    frame = 0
    origin = 128
    intensity = 5
    duration = 60
    speed = 3
    decay = 128
    while True:
        # Next test
        dTest = 1 if BtnRB.is_just_pressed else -1 if BtnLB.is_just_pressed else 0
        if dTest:
            return dTest

        if BtnA.is_just_pressed:
            frame = 0

        PPU.scanStart()
        
        for y in range(HEIGHT):
            dist = abs(y-origin)
            df = max(0.01,1-(dist/decay))
            wakeDist = frame * df * speed
            if dist < wakeDist:
                f = (wakeDist - dist) // (df * speed)
            else:
                f = 0
            
            t = max(0, 1 - (f / (df * duration)))
            dy = int((df * intensity) * t * math.sin(16*t*t))
            if y > origin:
                dy = -dy
            targetY = max(0,min(HEIGHT-1,y+dy))
            # print(y,targetY)
            layerWater.y = (targetY - y)
            PPU.scanLine(y)
        PPU.update()

        frame += 1
    

tests = [
    test_castle,
    test_river,
    test_shockwave,
]        

PPU.setFPS(30)

testIndex = 0
while True:
    testIndex = (testIndex + tests[testIndex]() + len(tests)) % len(tests)
    PPU.update()