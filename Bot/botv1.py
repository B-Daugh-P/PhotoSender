from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

from telegram import Update
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']


FOLDER_NAME, PHOTO, YN = '', 'd', 'yd'
counter = 0
filename = [None] * 50
filename[counter] = 'file_' + str(counter) + '.jpeg'
folder_id = ''
new_folder = True

start = '/start'
button_help = '/help'

def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    return build('drive', 'v3', credentials=creds)
def upload_files(filename):
    global folder_id, new_folder
    """
    Creates a folder and upload a file to it
    """
    # authenticate account
    service = get_gdrive_service()
    # folder details we want to make
    folder_metadata = {
        "name": FOLDER_NAME,
        "mimeType": "application/vnd.google-apps.folder"
    }
    if new_folder:#folder_id == '':
        # create the folder
        file = service.files().create(body=folder_metadata, fields="id").execute()
        # get the folder id
        new_folder = False
        folder_id = file.get("id")
        print("Folder ID:", folder_id)
        print("Folder Name:", FOLDER_NAME)
    # upload a file text file
    # first, define file metadata, such as the name and the parent folder ID
    file_metadata = {
        "name": filename,
        "parents": [folder_id]
    }
    # upload
    media = MediaFileUpload(filename, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print("File created, id:", file.get("id"))


def start_handler(update: Update, context: CallbackContext):
    global answ
    if new_folder:
        update.message.reply_text(
            text='Welcome to the PhotoSender bot!\nI will upload your photos to cloud storage.\nFor more info use "/help"\nTo start, supply the folder name, please.',
            reply_markup=ReplyKeyboardRemove(),
        )
        return FOLDER_NAME
    else:
        update.message.reply_text(
            text='Do you want to create new folder?(y/n)',
            reply_markup=ReplyKeyboardRemove(),
        )
        return YN
def disting_handler(update: Update, context: CallbackContext):
    global new_folder
    answ = update.message.text
    if answ == 'y':
        new_folder = True
        return start_handler(update= update, context= context)
    elif answ == 'n':
        update.message.reply_text(
            text='You can send photos now.',
        )
        return PHOTO
    else:
        update.message.reply_text(
            text='Please, enter y for Yes or n for No'
        )
        return start_handler(update= update, context= context)
def name_saver(update: Update, context: CallbackContext):
    global FOLDER_NAME
    FOLDER_NAME = update.message.text
    update.message.reply_text(
        text='You can send photos now.',
    )
    return PHOTO
def photo_handler(update: Update, context: CallbackContext):
    global counter, filename
    counter += 1
    filename[counter] = 'file_' + str(counter) + '.jpeg'
    obj = context.bot.getFile(file_id=update.message.photo[-1].file_id)
    obj.download(filename[counter])

    return PHOTO
def upload_handler(update: Update, context: CallbackContext):
    global filename, counter, FOLDER_NAME, PHOTO
    if counter != 0:
        for x in range(1, counter+1):
            print('File name: ' + filename[x])
            upload_files(filename=filename[x])
        update.message.reply_text(
            text='Done! \nUploaded ' + str(counter) + ' files.',
        )
        filename = [None] * 50
        counter = 0
        FOLDER_NAME, PHOTO = '', 'd'
        return ConversationHandler.END
    else:
        update.message.reply_text(
            text="Nothing to upload."
        )

def button_help_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="After the start command, supply a folder name of your choosing.\nAfter, you can start sending the photos.\n"
             "When you done with sending, just type '/upload' and I'll upload it to the cloud.", #How to use, add later
        reply_markup=ReplyKeyboardRemove(),
    )

def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    if text == button_help:
        return button_help_handler(update=update, context=context)
    elif text == '/upload':
        return upload_handler(update=update, context=context)

    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=start)
            ],
            [
                KeyboardButton(text=button_help)
            ],
        ],
        resize_keyboard=True,
    )


def main():
    print('Start')

    updater = Updater(
        token='1383428486:AAFFwKhidt-lFrK7Tsb6r1bgSqtOMcC7GKQ',
        use_context= True,
    )

    photoHandler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_handler),
        ],
        states={
            FOLDER_NAME: [
                MessageHandler(Filters.text, name_saver, pass_user_data= True),
            ],
            YN: [
                MessageHandler(Filters.text, disting_handler, pass_user_data= True),
            ],
            PHOTO: [
                MessageHandler(Filters.photo, photo_handler, pass_user_data= True)
            ],
        },
        fallbacks=[
            CommandHandler('upload', upload_handler),
        ],
    )

    updater.dispatcher.add_handler(photoHandler)
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=message_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
