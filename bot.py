import telebot
from telebot import types
from config import *
from download import *
from homework import *
from table import *
from gdz import *
from config import *

gdz_data = []
classes = ['5 класс', '6 класс', '7 класс', '8 класс', '9 класс', '10 класс', '11 класс']
timeOfFood = ["Завтрак", "Обед"]
bot = telebot.TeleBot("5974518842:AAF9W6oy8IvBd9FEGlKu6PWx1SNLbSIgLRU")

def some_error(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  btn1 = types.KeyboardButton("Скинь расписание")
  btn2 = types.KeyboardButton("Реши ДЗ")
  btn3 = types.KeyboardButton("Скинь ДЗ")
  btn4 = types.KeyboardButton("Че хаваем завтра")
  markup.add(btn1, btn2, btn3, btn4)
  bot.send_message(message.chat.id, text='Неизвестная ошибка', reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):  
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  btn1 = types.KeyboardButton("Скинь расписание")
  btn2 = types.KeyboardButton("Реши ДЗ")
  btn3 = types.KeyboardButton("Скинь ДЗ")
  btn4 = types.KeyboardButton("Че хаваем завтра")
  markup.add(btn1, btn2, btn3, btn4)
  bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я *VilgaBOT*, который сделает твою учебу проще.".format(message.from_user), parse_mode='Markdown')
  bot.send_photo(message.chat.id, photo=open('./assets/f.png', 'rb'))
  bot.send_message(message.chat.id, text="Выбери опцию, *используя кнопки*, которую ты хотел, чтобы я исполнил".format(message.from_user), reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def answers(message):
  if message.text == "Скинь расписание":
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("5 класс")
    button2 = types.KeyboardButton("6 класс")
    button3 = types.KeyboardButton("7 класс")
    button4 = types.KeyboardButton("8 класс")
    button5 = types.KeyboardButton("9 класс")
    button6 = types.KeyboardButton("10 класс")
    button7 = types.KeyboardButton("11 класс")
    markup.add(button1, button2, button3, button4, button5, button6, button7)
    bot.send_message(message.chat.id, text="Конечно, {0.first_name}! Выбери класс, чтобы получить расписание".format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, get_clas)
  elif message.text == "Реши ДЗ":
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button3 = types.KeyboardButton("Алгебра")
    markup.add(button3)
    bot.send_message(message.chat.id, text='Конечно, {0.first_name}! Выбери предмет, по которому ты хочешь получить решение'.format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, get_class)

  elif message.text == "Скинь ДЗ":
    try:
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      btn1 = types.KeyboardButton("Скинь расписание")
      btn2 = types.KeyboardButton("Реши ДЗ")
      btn3 = types.KeyboardButton("Скинь ДЗ")
      btn4 = types.KeyboardButton("Че хаваем завтра")
      markup.add(btn1, btn2, btn3, btn4)
      m = types.InlineKeyboardMarkup()
      bt1 = types.InlineKeyboardButton("Группа VK", url='https://vk.com/vilga_bot')
      m.add(bt1)
      get_hw()
      bot.send_photo(message.chat.id, photo=open(f'./outputs/hw {tomorrow()}.png', 'rb'))
      if len(get_hw()) != 0:
        bot.send_message(message.chat.id, text="Слишком длинное задание, вот полный текст:")
        bot.send_message(message.chat.id, text=get_hw(), getUploadFolder_mode= 'Markdown')
      else:
        bot.send_message(message.chat.id, text=f"Вот домашнее задание на {tomorrow()}", reply_markup=markup)
        bot.send_message(message.chat.id, text=f"Подписывайся на нашу группу в VK", reply_markup=m)
    except Exception as _ex:
      bot.send_message(message.chat.id, text=f'Неизвестная ошибка. Попробуй еще раз {_ex}')
  
  elif message.text == "Че хаваем завтра":
    try:
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      button1 = types.KeyboardButton("Завтрак")
      button2 = types.KeyboardButton("Обед")
      markup.add(button1, button2)
      bot.send_message(message.chat.id, text="Выбери время", reply_markup=markup)
      bot.register_next_step_handler(message, getTypeFood)
    except:
      bot.send_message(message.chat.id, text=f'Неизвестная ошибка. Попробуй еще раз')

def get_clas(message):   
  if message.text in classes:
    if type(getUploadFolder(tomorrow())) is not list:
      m = types.InlineKeyboardMarkup()
      bt1 = types.InlineKeyboardButton("Группа VK", url='https://vk.com/vilga_bot')
      m.add(bt1)
      classs = message.text.split(' ')[0]
      DownloadSchedule(tomorrow(), getUploadFolder(tomorrow()))
      get_img(tomorrow(), classs)
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      btn1 = types.KeyboardButton("Скинь расписание")
      btn2 = types.KeyboardButton("Реши ДЗ")
      btn3 = types.KeyboardButton("Скинь ДЗ")
      btn4 = types.KeyboardButton("Че хаваем завтра")
      markup.add(btn1, btn2, btn3, btn4)
      bot.send_message(message.chat.id, text=f"Вот расписание на ближайщую дату: {tomorrow()}", reply_markup=markup)
      bot.send_photo(message.chat.id, photo=open(f'./outputs/{tomorrow()} {classs}.png', 'rb'))
      bot.send_message(message.chat.id, text=f"Подписывайся на нашу группу в VK", reply_markup=m)
    else:
      classs = message.text.split(' ')[0]
      m = types.InlineKeyboardMarkup()
      bt1 = types.InlineKeyboardButton("Группа VK", url='https://vk.com/vilga_bot')
      m.add(bt1)
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      btn1 = types.KeyboardButton("Скинь расписание")
      btn2 = types.KeyboardButton("Реши ДЗ")
      btn3 = types.KeyboardButton("Скинь ДЗ")
      btn4 = types.KeyboardButton("Че хаваем завтра")
      markup.add(btn1, btn2, btn3, btn4)
      bot.send_message(message.chat.id, text=f"Расписание еще не выложили")
      today_date = getUploadFolder(tomorrow())[0]
      today_folder = getUploadFolder(tomorrow())[1]
      bot.send_message(message.chat.id, text=f"Вот расписание на последнюю доступную дату: {today_date}")
      DownloadSchedule(today_date, today_folder)
      get_img(today_date, classs)
      bot.send_photo(message.chat.id, photo=open(f'./outputs/{today_date} {classs}.png', 'rb'), reply_markup=markup)
      bot.send_message(message.chat.id, text=f"Подписывайся на нашу группу в VK", reply_markup=m)
  else:
    some_error(message)


def get_class(message):
  if message.text == "Алгебра":
    gdz_data.append(message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button3 = types.KeyboardButton("7 класс")
    button4 = types.KeyboardButton("8 класс")
    button5 = types.KeyboardButton("9 класс")
    button6 = types.KeyboardButton("10 класс")
    button7 = types.KeyboardButton("11 класс")
    markup.add(button3, button4, button5, button6, button7)
    bot.send_message(message.chat.id, text="Теперь выбери класс".format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, get_task)
  else:
    some_error(message)

def getTypeFood(message):
  if message.text in timeOfFood:
    m = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton("Группа VK", url='https://vk.com/vilga_bot')
    m.add(bt1)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Скинь расписание")
    btn2 = types.KeyboardButton("Реши ДЗ")
    btn3 = types.KeyboardButton("Скинь ДЗ")
    btn4 = types.KeyboardButton("Че хаваем завтра")
    markup.add(btn1, btn2, btn3, btn4)
    DownloadFood(FoodTime())
    FoodgetUploadFolderr(FoodTime(), message.text)
    bot.send_message(message.chat.id, text=f"Вот меню столовой на {FoodTime()}", reply_markup=markup)
    bot.send_photo(message.chat.id, photo=open(f'./outputs/{FoodTime()} food.png', 'rb'))
    bot.send_message(message.chat.id, text=f"Подписывайся на нашу группу в VK", reply_markup=m)
    

def get_task(message):
  gdz_data.append(message.text)
  a = telebot.types.ReplyKeyboardRemove()
  bot.send_message(message.chat.id, text='Последний шаг: напиши номер задания', reply_markup=a)
  bot.register_next_step_handler(message, final_sol)

def final_sol(message):
  gdz_data.append(message.text)
  try:
    classs = gdz_data[1].split(' ')[0]
    math(str(classs), str(gdz_data[2]))
    bot.send_photo(message.chat.id, photo=open(f'./outputs/{gdz_data[2]} {classs}.jpg', 'rb'))
    m = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton("Группа VK", url='https://vk.com/vilga_bot')
    m.add(bt1)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Скинь расписание")
    btn2 = types.KeyboardButton("Реши ДЗ")
    btn3 = types.KeyboardButton("Скинь ДЗ")
    btn4 = types.KeyboardButton("Че хаваем завтра")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, text=f"Вот решение на номер: {gdz_data[2]}", reply_markup=markup)
    bot.send_message(message.chat.id, text=f"Подписывайся на нашу группу в VK", reply_markup=m)
  except Exception as _ex:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Скинь расписание")
    btn2 = types.KeyboardButton("Реши ДЗ")
    btn3 = types.KeyboardButton("Скинь ДЗ")
    btn4 = types.KeyboardButton("Че хаваем завтра")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, text=f"Неизвестная ошибка. Попробуй еще раз {_ex}", reply_markup=markup) 
  #os.remove(f'{tomorrow()} {classs}.png') 
  # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  # btn1 = types.KeyboardButton("Скинь расписание")
  # btn3 = types.KeyboardButton("Кто тебя создал?")
  # markup.add(btn1, btn3)
  # bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я бот, который будет отправлять тебе расписание, чтобы ты не напрягался".format(message.from_user), reply_markup=markup)
  # bot.send_message(message.chat.id, text="Используй кнопки для коммуникации со мной")



# another functional
# @bot.message_handler(content_types=['voice'])
# def voice_checker(message):
#   bot.send_message(message.chat.id, text="А Буквы на что ?")
# @bot.message_handler(content_types=['new_chat_title'])
# def title_checker(message):
#   bot.send_message(message.chat.id, text="А старое название чем не нравилось ?")

bot.polling(none_stop=True, interval=0)



