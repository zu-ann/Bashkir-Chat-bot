# -*- coding: utf-8 -*-
import flask, telebot, conf, time, phrases, TF_session
from telebot import types

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
print("Created bot")

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(conf.WEBHOOK_SSL_CERT, 'r'))
print("Set webhook")

app = flask.Flask(__name__)

def write_logs(id, text, message):
    with open('logs.txt','a',encoding='utf') as f:
        f.write(time.strftime('%d.%m.%Y %X', time.localtime(message.date)) + '\t' + str(id) + ':\t' + text + '\n')

def check_commands(command_name, answer):
    @bot.message_handler(commands = [command_name])
    def send_answer(message):
        write_logs(message.chat.id, message.text, message)
        print("Replying to " + command_name)
        bot.send_message(message.chat.id, answer)
        write_logs('Bashkort_chatbot', answer, message)

check_commands('start', phrases.start)
check_commands('help', phrases.help)

@bot.message_handler(commands=['mark'])
def get_mark(message):
    write_logs(message.chat.id, message.text, message)
    markup = types.ReplyKeyboardMarkup(row_width=3,one_time_keyboard=1)
    itembtn1 = types.KeyboardButton('👎')
    itembtn2 = types.KeyboardButton('😐')
    itembtn3 = types.KeyboardButton('👍')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, phrases.mark, reply_markup=markup)

@bot.message_handler(regexp = '[👎😐👍]')
def read_marks(message):
    text = message.text
    if text == '👎':
        mark = 0
    elif text == '🙂':
        mark = 1
    else:
        mark = 2
    write_logs(message.chat.id, str(mark), message)

@bot.message_handler(regexp ='[a-gi-uwxzA-GI-UWXZ]+')
def other_language(message):
    write_logs(message.chat.id, message.text, message)
    bot.send_message(message.chat.id, phrases.wrong_language)
    write_logs('Bashkort_chatbot', phrases.wrong_language, message)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_answer(message):
    write_logs(message.chat.id, message.text, message)
    print("Started send_answer")
    answer_text = TF_session.answer_by_seq2seq(message.text)
    bot.send_message(message.chat.id, answer_text)
    write_logs('Bashkort_chatbot', answer_text, message)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'OK!'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

app.run(host=conf.WEBHOOK_HOST,
        port=conf.WEBHOOK_PORT,
        ssl_context=(conf.WEBHOOK_SSL_CERT, conf.WEBHOOK_SSL_PRIV),
        debug=True)