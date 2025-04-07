from Scripts.Misc.init import SCREEN
from Scripts.Misc.init import screen
import pygame

#Uses image sizes and their position relative to the screen
#to see if you clicked a button


def checkForClickInBounds(screenRatioX, screenRatioY, buttonsize:tuple[int,int], mousePos):
    xPos = SCREEN.current_w/screenRatioX - buttonsize[0]/2 #= -1/2 buttonsize accounts for centering the button
    yPos = SCREEN.current_h/screenRatioY

    if intWithin(xPos, mousePos[0], xPos + buttonsize[0]) and intWithin(yPos, mousePos[1], yPos + buttonsize[1]):
        return True

def intWithin(int0, intCheck, int1):
    if int0 <= intCheck and intCheck <= int1:
        return True
    else:
        return False