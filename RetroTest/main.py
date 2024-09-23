
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

bmpCastle = Bitmap("castle.bmp", Color.MAGENTA)
bmpCastleBG = Bitmap("castle_bg.bmp")
bmpTile = Bitmap("tile.bmp")

#
#   Test Bitmap Layer
#
def test_bitmapLayer():
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
        for i in range(HEIGHT):
            layerSky.x = int(skyX-bgX+r*math.sin(t+i/10))
            PPU.scanLine(i)
        PPU.update()
        
#
#   Test Sprite Layer
#
def test_spriteLayer():
    return 1 # TODO
        
tests = [
    test_bitmapLayer,
    test_spriteLayer
]        

PPU.setFPS(30)

testIndex = 0
while True:
    testIndex = (testIndex + tests[testIndex]() + len(tests)) % len(tests)
    PPU.update()