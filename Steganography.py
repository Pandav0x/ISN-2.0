from PIL import Image
import math

__all__ = ['getPngImage', 'getImageSize', 'getFileSize', 'genBinaryMask', 'readBitPacket', 'infuseByte', 'infuseFile', 'extractFile']

def getPngImage(path):
    file = Image.open(path)
    if file.format != "PNG":
        raise ValueError('Image shall be formatted as a png')
    image = file.convert('RGBA')
    file.close()
    return image

def getImageSize(image):
    return image.height * image.width * len(image.getBands())

def getFileSize(file):
    old = file.tell()
    file.seek(0, 2) # Go at the end
    size = file.tell()
    file.seek(old, 0) # Go to the
    return size

def readImageAsBytes(image):
    def byteGenerator(image):
        for pixel in image.getdata():
            for value in pixel:
                yield value

    # Parse the data and return it
    return bytearray(byteGenerator(image))

def genBinaryMask(*args, R=False):
    """meh"""
    mask = 0
    for i in range(len(args)):
        if args[i if not R else -1-i]:
            mask += 1 << i
    return mask

def evalBinaryMask(binary):
    """mehmeh"""
    return eval("0b" + binary)

def splitByN(seq, n):
    """mehmehmeh"""
    while seq:
        yield seq[:n]
        seq = seq[n:]

def getBit(bytes, pos):
    """Get a bit from an array of bytes, as if it was a bit array"""
    if pos < len(bytes) * 8:
        return bytes[pos // 8] & (1 << (pos % 8))
    else:
        return None

def putBit(bytes, bit, pos):
    """Put some bit at some place in some byte array"""
    if pos < len(bytes) * 8:
        i, j = pos // 8, pos % 8
        bytes[i] &= (255 ^ 1 << j)
        if bit:
            bytes[i] |= (1 << j)
        return bytes[i]
    else:
        return None

def infuseBitInArray(bytes, bit, pos, n):
    return putBit(bytes, bit, 8 - n + pos // n * 8 + pos % n)

def readBitPacket(bytes, n, packet=0):
    """Read packet n°(packet) formed of (n) bits
    returns (None) if no more packets are available"""
    if n > 8:
        raise ValueError("can't split more than 8 bit")

    if (packet * n / 8) > len(bytes):
        return None # End marker

    value = 0
    for i in range(n):
        j = n * packet + i

        # Get the bit and construct the value
        if getBit(bytes, j):
            value += (1 << i)

    return value

def infuseByte(byte, packet):
    pass

def infuseFile(image, file, n):
    """file has to be opened as binary read"""
    if 'b' not in file.mode:
        raise ValueError('file shall be opened in binary mode at least')

    # The bytes to use if writing only on the n last bits
    infusingSize = lambda x, n: math.ceil(x * 8 / n)

    # Image, file and data size
    imageSize = getImageSize(image)
    fileSize = getFileSize(file)
    dataSize = infusingSize(fileSize, n)

    # Space partition in the image
    countFullSize = 4 # byte length to write the number
    countSize = infusingSize(countFullSize, n) # bytes used to really write
    availableSize = fileSize - countSize # remaining bytes to write

    if dataSize > availableSize:
        raise Exception('file is too big to be infused (%d/%d with %d)' % (dataSize, availableSize, n))

    # Byte arrays
    OUT = readImageAsBytes(image)
    IN = file.read()

    # Current bit position for writing into the image data
    wPosition = 0

    # Byte sequence representing the number of bytes encoded
    bCount = fileSize.to_bytes(countFullSize, 'big')

    # Write the numbers of bytes to infuse
    for i in range(countFullSize * 8):
        bit = getBit(bCount, wPosition)
        infuseBitInArray(OUT, bit, wPosition, n)
        wPosition += 1

    bit = True # Bit to copy
    rPosition = 0 # Position relative to reading
    while bit is not None:
        bit = getBit(IN, rPosition)
        if bit is None: break
        infuseBitInArray(OUT, bit, wPosition, n)

def extractFile(imagePath):
    pass
    
    """ # OLD
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
    """
