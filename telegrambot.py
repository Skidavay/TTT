import telebot
import requests
import json

TOKEN = "6244495882:AAEU22TFxNIBoMmDqwOmD6gSw3sCs8yooVs"
bot = telebot.TeleBot(TOKEN)

keys = {
    'биткоин': 'BTC',
    'эфириум': 'ETH',
    'доллар': 'USD',
    'рубль': 'RUR',
    'евро': 'EUR',
}

class ConvertionException(Exception):
    pass


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Welcome, {message.chat.username}")

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Что бы начать работу введите команду боту в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \nУвидеть список доступных валют - /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n' .join((text, key))
    bot.reply_to(message, text)



@bot.message_handler(content_types=['photo', ])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, 'Nice meme XDD')

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    if len(values) > 3:
        raise ConvertionException('Слишком много параметров')

    quote, base, amount = values
    quote_ticker, base_ticker = keys[quote], keys[base]

    if quote == base:
        raise(ConvertionException(f'Невозможно перевести одинаковые валюты{base}'))

    try:
        quote_ticker = keys[quote]
    except KeyError:
        raise ConvertionException(f'Не удалось обработать валюту{quote}')

    try:
        base_ticker = keys[base]
    except KeyError:
        raise ConvertionException(f'Не удалось обработать валюту {base}')

    try:
        amount = float(amount)
    except ValueError:
        raise ConvertionException(f'Не удалось обработать количество{amount}')

    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
    total_base = json.loads(r.content)[keys[base]]
    text = f'Цена {amount} {quote} в {base}: {total_base}'
    bot.send_message(message.chat.id, text)


bot.polling()
