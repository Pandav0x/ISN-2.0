import functions

textPath = r".\text.txt"
imagePath = r".\image.png"
imagePathDec = r".\crypted_image.png"

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
