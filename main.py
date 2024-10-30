import telebot
from telebot import types

bot = telebot.TeleBot("7861726729:AAHaewmqWXT5cnYe3ucLLNWxZ8vv-mctQB4")
name = ''
surname = ''
age = 0


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(5):
        key = types.InlineKeyboardButton(text=f'И{i}', callback_data=f'{i}')
        keyboard.add(key)
    text = ("Выбери какое изображене вывести."
            "\nНапиши выбрать аудиофайл для вывода списка аудиофалов.")
    bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == 'выбрать аудиофайл':
        keyboard = types.InlineKeyboardMarkup()
        for i in range(5):
            key = types.InlineKeyboardButton(text='А{i}', callback_data='{i}')
            keyboard.add(key)
        bot.send_message(message.from_user.id, "Выбирете аудиофайл", reply_markup=keyboard)



def get_name(message): #получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    try:
        age = int(message.text) #проверяем, что возраст введен корректно
    except Exception:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
    keyboard = types.InlineKeyboardMarkup() # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Запомню : )')


bot.polling(none_stop=True, interval=0)
