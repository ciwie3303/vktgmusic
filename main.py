
import vk_api
from vk_api.audio import VkAudio
import requests
import telebot
from colored import fg, bg, attr
from telebot import types

vk_session = vk_api.VkApi('+', '') #логин и пароль
vk_session.auth()
vkaudio = VkAudio(vk_session)


bot = telebot.TeleBot('1899908252:AAGruHfjnNkmvtnqsHQ2UCakxcw2LhEvXks') #токен
channel = "-1001446655349" # id канала
link_tgchannel = "https://t.me/vktgmusic" # Ссылка на телеграм канал

check = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
but1 = types.KeyboardButton("Проверить подписку")
check.add(but1)


@bot.message_handler(commands=['start'])
def welcome(message):
  bot.send_message(message.chat.id,  text = link_tgchannel+"\nПодпишитесь для использования бота", reply_markup=check)
  print("{}[LOG]{}".format(bg("#00FFFF"), attr("reset")), message.from_user.first_name, "зашел в бота" )



@bot.message_handler(commands=['music'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id,'скинь id от вк , пример - 180914267')
    bot.register_next_step_handler(msg, _music)
    print("{}[LOG]{}".format(bg("#00FFFF"), attr("reset")), message.from_user.first_name, "ввел команду" )

def _music(message):
    try:
        for track in vkaudio.get_iter(owner_id=int(message.text)): # тут id свое
            bot.send_audio(message.chat.id,  f"{track.get('url')} ")
    except:
        bot.send_message(message.chat.id,'норм id введи\nповторно кинуть запрос введи /music')

@bot.message_handler(commands=['search'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id,'Название песни введи')
    bot.register_next_step_handler(msg, _music_s)

def _music_s(message):
    for track in vkaudio.search(q=message.text, count=3, offset=0): #тут запрос свой 
       bot.send_audio(message.chat.id, f"{track.get('url')}")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
  if message.text == "Проверить подписку":
    status = ['creator', 'administrator', 'member']
    for i in status:
      if i == bot.get_chat_member(chat_id=channel, user_id=message.from_user.id).status:
        chat_id = message.chat.id
        bot.send_message(chat_id, "Подписка найдена.\n\nвассап.\n\n/music - парсит всю свою музыку со страницы\n/search - только по запросу скинет песни\n\nСтраница и музыка должны быть открыты'")
        break
    else:
      chat_id = message.chat.id
      bot.send_message(chat_id, text = "Подписка не найдена.")

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)  
