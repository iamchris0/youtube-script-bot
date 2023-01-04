import telebot

from utils import download_video, download_audio, send_file
from app import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def msg_start(message):
    text = "Привет, пришли мне ссылку на видео!"
    bot.send_message(
        chat_id=message.from_user.id,
        text=text
    )


@bot.message_handler(content_types=["text"])
def get_url(message):
    url = message.text

    message = bot.send_message(
        chat_id=message.chat.id,
        text='Приступаю к скачиванию видео!'
    )

    try:
        download_video(url, bot, message)
        try:
            send_file(bot=bot, msg=message, typ='video')
        except Exception as e:
            print(e)
            message = bot.send_message(
                chat_id=message.chat.id,
                text='При отправке видео возникла ошибка, попробуйте снова.'
            )
    except Exception:
        message = bot.send_message(
            chat_id=message.chat.id,
            text='При загрузке видео возникла ошибка, попробуйте снова.'
        )

    try:
        download_audio(url)
        try:
            send_file(bot=bot, msg=message, typ='audio')
        except Exception:
            bot.send_message(
                chat_id=message.chat.id,
                text='При отправке аудио возникла ошибка, попробуйте снова.'
            )
    except Exception:
        bot.send_message(
            chat_id=message.chat.id,
            text='При загрузке аудио возникла ошибка, попробуйте снова.'
        )


bot.polling(none_stop=True)
