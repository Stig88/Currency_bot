import telebot
from config import TOKEN, keys
from extensions import Converter, APIException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_(message: telebot.types.Message):
    text = '''Привет! Я показываю стоимость указываемого количества валюты в другой валюте. \n 
Умею работать c записью формата <базовая валюта><котируемая валюта><количество базовой валюты>. \n
Принимаются названия на русском. Ввод нечувствителен к регистру. Пример запроса - по команде /help. \n
Список валют - /values.'''
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help_(message: telebot.types.Message):
    text = '''"Рубль доллар 105.65" - сколько долларов можно купить на 105 рублей 65 копеек.
"Доллар рубль" - актуальный курс доллара к рублю'''
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values_(message: telebot.types.Message):
    text='Список валют: '
    for name, code in keys.items():
        text += f'{code}, {name}\n'
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) < 2 or len(values) > 3:
            raise APIException('Неправильное число параметров!')

        base = values[0]
        quote = values[1]
        amount = 1

        if len(values) == 3:
            try:
                amount = float(values[2])
            except ValueError:
                raise APIException(f'Проверьте запись "{values[2]}" (требуется цифровое указание количества)')

        total_quote = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        result=f'Цена в {keys[quote]} за {amount} {keys[base]} = {total_quote}'
        bot.send_message(message.chat.id, result)


bot.polling()