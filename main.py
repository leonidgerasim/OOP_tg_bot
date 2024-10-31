import telebot
from telebot import types
import os

bot = telebot.TeleBot("7861726729:AAHaewmqWXT5cnYe3ucLLNWxZ8vv-mctQB4")
image_list = [image[:-4] for image in os.listdir('images')]
audio_list = [audio[:-4] for audio in os.listdir('audio')]


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text='Выбрать изображение', callback_data='image')
    keyboard.add(key)
    key = types.InlineKeyboardButton(text='Выбрать аудиофайл', callback_data='audio')
    keyboard.add(key)
    text = 'Выбирете что вывести\nНапишите /get чтобы получить ссылку на репозиторий'
    bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)


@bot.message_handler(commands=['get'])
def get(message):
    bot.send_message(message.from_user.id, text='https://github.com/leonidgerasim/OOP_tg_bot.git')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'image':
        keyboard = types.InlineKeyboardMarkup()
        for image in image_list:
            key = types.InlineKeyboardButton(text=image, callback_data=image)
            keyboard.add(key)
        text = 'Выбирете изображение'
        bot.send_message(call.message.chat.id, text=text, reply_markup=keyboard)
    elif call.data == 'audio':
        keyboard = types.InlineKeyboardMarkup()
        for audio in audio_list:
            key = types.InlineKeyboardButton(text=audio, callback_data=audio)
            keyboard.add(key)
        text = 'Выбирете трек'
        bot.send_message(call.message.chat.id, text=text, reply_markup=keyboard)
    elif call.data in image_list:
        bot.send_photo(call.message.chat.id, photo=open('images/' + call.data + '.png', 'rb'))
    elif call.data in audio_list:
        bot.send_audio(call.message.chat.id, audio=open('audio/' + call.data + '.mp3', 'rb'))


bot.polling(none_stop=True, interval=0)
