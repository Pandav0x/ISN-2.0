import string
from math import *
from PIL import Image

#image
def getImage(imagePath):
    imageFile = Image.open(imagePath)
    if(imageFile.format != "PNG"):
        quit()
    image = imageFile.convert('RGBA')
    imageFile.close()
    return image

#text
def getText(textPath):
    textFile = open(textPath, 'r')
    text = textFile.read().replace("œ", "oe")
    textFile.close()
    return text


def crypt(textPath, imagePath):
    image = getImage(imagePath)
    text = getText(textPath)
    if(text.count("") <= image.size[0]*image.size[1]):
        print("Text will fit in pic")
        image.putpixel((0,0), (text.count("")&255,text.count("")>>8&255,text.count("")>>16&255,text.count("")>>24&255))
        for i in range(1, text.count("")-1): #\0 at end
            r, g, b, a = image.getpixel((i%(image.size[0]), floor(i/(image.size[0]))))
            tTemp = ord(text[i])
            image.putpixel((i%(image.size[0]), floor(i/(image.size[0]))),(r-(r%4)+(tTemp&192)%63, g-(g%4) + (tTemp&48)%15, b-(b%4) + (tTemp&12)%3, a-(a%4) + tTemp%3))
        image.save("crypted_image.png")
    else:
        print("Text will not fit in pic")

#WIP
def uncrypt(imagePath):
    image = getImage(imagePath)
    r, g, b, a = image.getpixel((0,0))
    lNumber = (r + (g*(2**8)) + (b*(2**16)) + (a*(2**24))) -1
    txt = ""
    for i in range(1, lNumber):
        r, g, b, a = image.getpixel((i%(image.size[0]), floor(i/(image.size[0]))))
        tmp = (a%4)&3 | ((b%4)&12)<<2 | ((g%4)&48)<<4 | ((r%4)&192)<<6 #nope
        print("Temp value: ", tmp)
        txt += chr(tmp)

    print(txt)
