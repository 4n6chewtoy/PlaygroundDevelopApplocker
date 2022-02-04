# PlaygroundDevelopApplockerDecrypt
A python script to decrypt media files encrypted using the Android application 'Apps Lock &amp; File Encryption — GOLD version’ (https://play.google.com/store/apps/details?id=playground.develop.applocker).
Original Blog Post: https://theincidentalchewtoy.wordpress.com/2021/12/12/decrypting-apps-lock-file-encryption-gold-version/

‘Apps Lock & File Encryption — GOLD version’ is a secure application which allows users to protect their ‘data with file encryption and decryption.'

## Script Usage

Script takes 3 arguments:

1. Data folder (/data/data/playground.develop.applocker)
2. Encrypted media folder (/sdcard/applocker)
3. Output folder

If the script cannot find key file it will exit.

As the lock for the application is not required for decryption the script does not retrieve it. However, it can be found in the 'applocker.db' database file.

This code is already intergrated into ALEAPP (https://github.com/abrignoni)

Any questions, or issues let me know https://twitter.com/4n6chewtoy
