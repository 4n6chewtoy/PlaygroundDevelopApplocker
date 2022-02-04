####
# A python script to decrypt media files encrypted using the Android application 
# 'Apps Lock & File Encryption — GOLD version’.
# Original blog post: https://theincidentalchewtoy.wordpress.com/2021/12/12/decrypting-apps-lock-file-encryption-gold-version/
###

### Import required modules
import sys
import os
import xml.etree.ElementTree as ET
import base64
import filetype
from Crypto.Cipher import AES
from pathlib import Path

### Inputs
## The '/data/data/playground.develop.applocker' folder
cwd = sys.argv[1]
## The '/sdcard/applocker' folder
mediaInputFolder = sys.argv[2]
## The output folder. 
outputFolder = sys.argv[3]

### Check if the preferences file required exists
### Loop checking the folders
if('shared_prefs' in next(os.walk(cwd))[1]):
    ### If shared_preferences folder exisits, check for the file 'com.domobile.applockwatcher_preferences.xml'
    if(os.path.join(cwd, 'shared_prefs\crypto.KEY_256.xml')):
        shared_prefs = (os.path.join(cwd, 'shared_prefs\crypto.KEY_256.xml'))
        ### If the file exisits, read the contents of <string name="cipher_key">
        tree = ET.parse(shared_prefs)
        root = tree.getroot()
        # From base64 to hex
        key = base64.b64decode(root.findall('./string[@name="cipher_key"]')[0].text)
        print('\n------------------------------------------')
        print(f'Key Identified:\t{key}')
        print('------------------------------------------')
else:
    print('\n------------------------------------------')
    print("Could not find the key, exiting...")
    print('------------------------------------------')
    exit
        
### Media folder traversal
mediaFolder = [x[0] for x in os.walk(mediaInputFolder) if "vault" in x[0]]
if not mediaFolder:
    print('------------------------------------------')
    print('\nCould not find media folder, exiting...\n')
    print('------------------------------------------')
else:
    print('\n------------------------------------------')
    print('Attempting to Decrypt Files')
    print('------------------------------------------')
    ### Deal with output folder creation
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
        print("Made output folder")
    else:
        print("Output folder alreay exists, will use this instead")
    ### For each file in the input folder    
    for files in os.listdir(mediaFolder[0]):
        print('\n------------------------------------------')
        print('Found file...\n')
        currentFile = os.path.join(mediaFolder[0], files)
        print(currentFile)
        print('------------------------------------------')
        with open (currentFile, 'rb') as openFile:
            print('Atttempting to decrypt...')
            fullFile = openFile.read()
            ### IV is after the first 2 bytes
            IV = fullFile[2:14]
            ### Following IV encrypted data minus the GCM validation (16 bytes) at the end
            encryptedData = fullFile[14:-16]
            ### New encryption algo
            cipher = AES.new((key), AES.MODE_GCM, (IV))
            ### Decrypt the data
            decryptedData = cipher.decrypt((encryptedData))
            ### Determine the correct file extension
            fileExtension = filetype.guess(decryptedData)
            ### Open the new output file for writing
            with open (os.path.join(outputFolder, Path(currentFile).stem + f'.{fileExtension.extension}'), 'wb') as decryptedFile:
                decryptedFile.write(decryptedData)
                decryptedFile.close()
                print("File decrypted and saved")
            
