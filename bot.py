from telebot import TeleBot
from telebot.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardRemove,
    WebAppInfo,
    BotCommand,
)
import json
from urllib.parse import quote as urlparse
from api_token import API_TOKEN
import requests


WEBAPP_URL = "https://mysite-simple-website.squareweb.app/"

def dict_to_url_params(params: dict):
    # escape characters that are not allowed in url
    # example: {'name': 'John Doe?'} -> 'name=John%20Doe%3F'
    return "?" + '&'.join([f'{ urlparse(key) }={ urlparse(value) }' for key, value in params.items()])


def markup_webapp_button(text, baseurl, params: dict = None):
    url = baseurl + dict_to_url_params(params) if params else baseurl
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton(text, web_app=WebAppInfo(url=url)))
    return markup


bot = TeleBot(API_TOKEN)


bot.set_my_commands(
    [
        BotCommand('start', 'Start the bot'),
        BotCommand('about', 'About / Sobre')
    ]
)


# WebApp messages handler
@bot.message_handler(content_types="web_app_data")
def answer(wmsg):
    userid = wmsg.from_user.id
    try:
        response = json.loads(wmsg.web_app_data.data)
        # clear keyboard
        bot.send_message(wmsg.from_user.id, 'Success! Data received: \n\n' + str(response), reply_markup=ReplyKeyboardRemove())

        action = response.get('action')

        if action == 'help':
            Help(userid, bot)
        elif action == 'sendData':
            ReceiveData(userid, bot, response.get('data'))
        elif action == 'randomImage':
            RandomImage(userid, bot)

    except Exception as e:
        print("#Error", e)
        response = wmsg.web_app_data.data
        bot.send_message(wmsg.from_user.id, 'Error, but data: \n\n' + response)


# Any messages handler
@bot.message_handler(func= lambda msg: True)
def any(msg):
    userid = msg.from_user.id
    initial_markup = InlineKeyboardMarkup()
    initial_markup.add(InlineKeyboardButton('🇺🇸 Start empty webapp | 🇧🇷 Iniciar webapp vazio', callback_data='start_webapp'))
    initial_markup.add(InlineKeyboardButton('🇺🇸 Send data to webapp | 🇧🇷 Enviar dados ao webapp', callback_data='get_info_to_webapp'))
    bot.send_message(userid, 'Hello, world!', reply_markup= initial_markup)


@bot.message_handler(commands=['about'])
def about(msg):
    userid = msg.from_user.id
    msg = "🇧🇷 Este é um bot simples que mostra como usar o webapp para enviar dados para o bot.\n\n"
    msg += "🇺🇸 This is a simple bot that shows how to use webapp to send data to the bot.\n\n"
    msg += "Repositório / Repository: https://github.com/arthurrogado/WebApp-Telegram-Bot\n"
    msg += "Contact me / Contate-me: @arthurrogado"
    bot.send_message(userid, msg)


@bot.callback_query_handler(func= lambda call: True)
def callback(call):
    userid = call.from_user.id
    if call.data == 'start_webapp':
        bot.send_message(userid, '🇧🇷 Clique no botão para acessar o webapp \n 🇺🇸 Click the button to open webapp', reply_markup= markup_webapp_button('Site', WEBAPP_URL) )
    elif call.data == 'get_info_to_webapp':
        Form(userid, bot)


class Form():
    def __init__(self, userid, bot: TeleBot) -> None:
        self.userid = userid
        self.bot = bot
        self.start_form()
        pass

    def start_form(self):
        msg = bot.send_message(self.userid, '🇺🇸 Whats your name? \n🇧🇷 Qual o seu nome?')
        bot.register_next_step_handler(msg, self.get_name)

    def get_name(self, msg):    
        self.name = msg.text
        msg = bot.send_message(self.userid, '🇺🇸 Your age? \n🇧🇷 Qual a sua idade?')
        bot.register_next_step_handler(msg, self.get_age)

    def get_age(self, msg):
        self.age = msg.text
        bot.send_message(self.userid, f' Name|Nome: {self.name}\n Age|Idade: {self.age}')

        data = {
            'name': self.name,
            'age': self.age,
        }
        bot.send_message(self.userid, '🇧🇷 Clique no botão para acessar o webapp \n 🇺🇸 Click the button to open webapp', reply_markup= markup_webapp_button('Site', WEBAPP_URL, data) )


class Help():
    def __init__(self, userid, bot: TeleBot) -> None:
        self.userid = userid
        self.bot = bot
        self.help()
        pass

    def help(self):
        msg = "🇧🇷 Este é um exemplo de mensagem de ajuda que poderia representar qualquer conteúdo fornecido pelo bot a partir do webapp"
        msg += "🇺🇸 This is a help message example that could represents any content provided by the bot from webapp.\n\n"
        self.bot.send_message(self.userid, msg)


# Classes that execute actions in a scope

class ReceiveData():
    def __init__(self, userid, bot: TeleBot, data) -> None:
        self.userid = userid
        self.bot = bot
        self.data = data
        self.receive_data()
        pass

    def receive_data(self):
        msg = "🇧🇷 Esta é uma mensagem com dados recebidos do webapp.\n"
        msg += "🇺🇸 This is a message with data received from webapp.\n\n"
        msg += "Data: " + str(self.data) + '\n\n'
        msg += f"Name/Nome: {self.data.get('name')}\n Age/Idade: {self.data.get('age')}"
        self.bot.send_message(self.userid, msg)


class RandomImage():
    def __init__(self, userid, bot: TeleBot) -> None:
        self.userid = userid
        self.bot = bot
        self.random_image()
        pass

    def random_image(self):
        self.bot.send_chat_action(self.userid, 'upload_photo')
        msg = "🇧🇷 Enviando uma mensagem com uma imagem aleatória recebida do webapp.\n\n"
        msg += "🇺🇸 Sending a message with a random image received from webapp.\n\n"
        self.bot.send_message(self.userid, msg)
        response = requests.get('https://source.unsplash.com/random')
        self.bot.send_photo(self.userid, response.content)


bot.infinity_polling()