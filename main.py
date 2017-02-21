import functions

#these are working paths
textPath = r"C:\Files\Programming\\Python\ISN2\text.txt"
imagePath = r"C:\Files\Programming\Python\ISN2\image.png"

imagePathDec = r"C:\Files\Programming\Python\ISN2\crypted_image.png"

#processing
while True:
    choice = input("Uncrypt or crypt? (U/C): ")
    if(choice in ["c", "C"]):
        functions.crypt(textPath, imagePath)
        break
    elif(choice in ["u", "U"]):
        functions.uncrypt(imagePathDec)
        break
    else:
        print("This is not an option.")
print("Done.")
