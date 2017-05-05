from PIL import Image
import math

"""
On va partir du principe que les images sont en RGBA, et on fera tout en RGBA, pour le moment.
"""

__all__ = ['getPngImage', 'getImageSize', 'getFileSize', 'genBinaryMask', 'readBitPacket', 'infuseByte', 'infuseFile', 'extractFile']

HEADER_SIZE = 4
INFUSING_SIZE = 2

class InfusionException(Exception): pass

def getPngImage(path):
    file = Image.open(path)
    if file.format != "PNG":
        raise ValueError('Image shall be formatted as a png')
    image = file.convert('RGB')
    file.close()
    return image

def getImageSize(image):
    return image.height * image.width * len(image.getbands())

def getFileSize(file):
    old = file.tell()
    file.seek(0, 2) # Go at the end
    size = file.tell()
    file.seek(old, 0) # Go to the last position
    return size

def getBit(bytes, pos):
    return bytes[pos // 8] >> (pos % 8) & 1

def putBit(bytes, pos, val):
    bytes[pos // 8] ^= (-val ^ bytes[pos // 8]) & (1 << pos % 8)

def putInfusedBit(bytes, pos, val):
    putBit(bytes, 8 * (pos // INFUSING_SIZE) - (8 - INFUSING_SIZE + pos % INFUSING_SIZE), val)

def getInfusedBit(bytes, pos):
    return getBit(bytes, 8 * (pos // INFUSING_SIZE) - (8 - INFUSING_SIZE + pos % INFUSING_SIZE))

def infuseFile(fileIn, imageIn, imageOut):
    file = open(fileIn, 'br')
    fileSize = getFileSize(file)

    dataSize = fileSize + HEADER_SIZE
    requiredBytes = dataSize * INFUSING_SIZE

    image = getPngImage(imageIn)
    imageSize = getImageSize(image)

    if requiredBytes > imageSize:
        raise InfusionException('Data too big')

    HEADER = int.to_bytes(fileSize, HEADER_SIZE, 'big')
    BODY = file.read()
    file.close()

    DATA = HEADER + BODY
    PIXELS = bytearray((value for pixel in image.getdata() for value in pixel))

    for i in range(dataSize * 8):
        putInfusedBit(PIXELS, i, getBit(DATA, i))

    infusedImage = Image.frombytes('RGB', image.size, bytes(PIXELS))
    infusedImage.save(imageOut)

def extractFile(imageIn, fileOut):
    image = getPngImage(imageIn)
    PIXELS = bytearray((value for pixel in image.getdata() for value in pixel))
    HEADER = bytearray(HEADER_SIZE)

    for i in range(HEADER_SIZE * 8):
        putBit(HEADER, i, getInfusedBit(PIXELS, i))

    dataSize = int.from_bytes(HEADER, 'big')

    BODY = bytearray(dataSize)
    for i in range(dataSize * 8):
        putBit(BODY, i, getInfusedBit(PIXELS, i + HEADER_SIZE * 8))

    file = open(fileOut, 'bw')
    file.write(BODY)
    file.close()
