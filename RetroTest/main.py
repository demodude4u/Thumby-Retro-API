
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

bmpTile = Bitmap("tile.bmp")

#
#   Test Bitmap Layer
#
def test_bitmapLayer():
    layerBG = BitmapLayer(bmpTile)
    PPU.layers = [
        layerBG
    ]

    x = 0
    t = 0
    while True:
        # Next test
        if BtnMENU.is_just_pressed:
            break
        
        x -= 0.75
        layerBG.y += 1
        t += 0.1
        for i in range(HEIGHT):
            layerBG.x = int(x+5*math.sin(t+i/20))
            PPU.scanLine(i)
        PPU.update()
        
tests = [
    test_bitmapLayer
]        

PPU.setFPS(30)
while True:
    for test in tests:
        test()
        PPU.update()