from pytube import YouTube
import os
import glob


def download_video(source, bot, msg):
    youtubobject = YouTube(source)
    youtubobject.streams.filter(res="360p").first().download()
    if len(glob.glob('*.mp4')) > 0:
        bot.delete_message(
            chat_id=msg.chat.id,
            message_id=msg.message_id
        )


def download_audio(source):
    youtubobject = YouTube(source)
    youtubobject.streams.filter(only_audio=True, file_extension='mp4').first().download()


def convert_bytes(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            if x in ['GB', 'TB']:
                return False
            elif (x == 'MB') and float(size) < 50:
                return True
            else:
                return True
        size /= 1024.0


def send_file(bot, msg, typ):
    title = os.path.abspath(glob.glob('*.mp4')[0])
    if typ == 'audio':
        if not convert_bytes(os.path.getsize(title)):
            bot.send_message(
                chat_id=msg.chat.id,
                text='Ваше аудио слишком большого размера, поэтому не может быть отправлено :('
            )
        else:
            bot.send_message(
                chat_id=msg.chat.id,
                text='Ваше аудио 👇'
            )
            bot.send_audio(
                chat_id=msg.chat.id,
                audio=open(title, 'rb')
            )
    else:
        if not convert_bytes(os.path.getsize(title)):
            bot.send_message(
                chat_id=msg.chat.id,
                text='Ваше видео слишком большого размера, поэтому не может быть отправлено :('
            )
        else:
            bot.send_message(
                chat_id=msg.chat.id,
                text='Ваше видео 👇',
            )
            bot.send_video(
                chat_id=msg.chat.id,
                video=open(title, 'rb')
            )
    os.remove(title)
