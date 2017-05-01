import Steganography as S

textIn = r".\text.txt"
textOut = r".\decrypted_text.txt"

imageIn = r".\image.png"
imageOut = r".\crypted_image.png"

while True:
    choice = input("Uncrypt or crypt? (U/C): ")
    if(choice in ["c", "C"]):
        S.infuseFile(textIn, imageIn, imageOut)
        break
    elif(choice in ["u", "U"]):
        S.extractFile(imageOut, textOut)
        break
    else:
        print("This is not an option.")
print("Done.")
