# PhotoSender
Telegram Bot to send  picturest from Telegram chats to Google Drive.


The bot that is uploaded to repo will send photos to my Drive. To send it to Drive of your choosing, follow the tutorial bellow.




First of all, delete files "credetials.json" and "token.pickle" from your working directory.


To use the bot, you will have to download python scripts, libraries and run them from your computer.
First, you need to install python itself on your computer. After, you will need any IDE that will run python scripts.

After you have your environment set up, you'll need to download python-telegram-bot library. To dO that, go to your IDE and, in the Python Console type this command: 
pip install python-telegram-botturn.

After the library is installed, you will need to turn on your Drive API and run sample script in python.(https://developers.google.com/drive/api/v3/quickstart/python)

In order for the script to run properly, please ensure ther is a .txt file in your working directory called "api_test1.txt". It can contain anything. This file will be uploaded to your drive as a test.

When you have your API set up and you ran the sample python script, you can start the bot. (To see, if sample script worked, in your Drive should be a folder named TestFolder with file api_test1.txt in it.)

Just run the script named botv1.py and you can use the bot.
