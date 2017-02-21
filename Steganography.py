from PIL import Image

__all__ = ['getPngImage', 'getImageSize', 'getFileSize', 'infuse', 'extract']

def getPngImage(path):
    file = Image.open(path)
    if file.format != "PNG":
        raise ValueError('Image shall be formatted as a png')
    image = file.convert('RGBA')
    file.close()
    return image

def getImageSize(image):
    return image.size[0] * image.size[1]

def getFileSize(file):
    old = file.tell()
    file.seek(0, 2) # Go at the end
    size = file.tell()
    file.seek(old, 0) # Go to the
    return size

def infuse(image, file):
    """file has to be opened as binary read"""
    if 'b' not in file.mode:
        raise ValueError('file shall be opened in binary mode at least')

    fileSize = getFileSize(file)
    while file.tell() < fileSize:
        print('pouet')

    """ # OLD
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
    """

def extract(imagePath):
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
