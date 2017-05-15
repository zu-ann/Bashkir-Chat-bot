# -*- coding: utf-8 -*-
import flask, telebot, re, conf, json, random, time, translate

import tensorflow as tf

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

regUNK = re.compile('_UNK')

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
print("created bot")

# удаляем предыдущие вебхуки, если они были
bot.remove_webhook()
time.sleep(2)
# ставим новый вебхук = Слышь, если кто мне напишет, стукни сюда — url
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(conf.WEBHOOK_SSL_CERT, 'r'))
print("set webhook")

app = flask.Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print("started send_welcome")
    bot.send_message(message.chat.id, "Здравствуйте! Это бот на башкирском.")


def read_files():
    f1 = open('Sample_answers.json', 'r', encoding='UTF-8')
    f2 = open('Regex.json', 'r', encoding='UTF-8')
    f3 = open('Offensive_words.json', 'r', encoding='UTF-8')
    sample_answers = json.load(f1)
    regex = json.load(f2)
    offensive_words = json.load(f3)
    regex['offensive_words'] = offensive_words
    print("opened files")
    f1.close()
    f2.close()
    f3.close()
    return sample_answers, regex

@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_sample_answers(message):
    print("started send_sample_answers")
    sample_answers, regex = read_files()
    text = message.text
    answer = 0
    for lst in regex:
        for elem in regex[lst]:
            res = re.search(elem, text)
            if res:
                if not lst.endswith('greeting') and not lst.endswith('goodbye'):
                    lst += '_answer'
                elif lst == 'formal_greeting':
                    hour = int(time.strftime('%H', time.gmtime(message.date))) + 3
                    if 4 <= hour < 12:
                        print(hour)
                        sample_answers[lst].append('Хәйерле иртә! (доброе утро)')
                        print('Хәйерле иртә! (доброе утро)')
                    if 12 <= hour <= 16:
                        print(hour)
                        sample_answers[lst].append('Хәйерле көн! (добрый день)')
                        print('Хәйерле көн! (добрый день)')
                    if 16 < hour <= 22:
                        print(hour)
                        sample_answers[lst].append('Хәйерле кис! (добрый вечер)')
                        print('Хәйерле кис! (добрый вечер)')
                    if hour > 22 or hour < 4:
                        print(hour)
                        sample_answers[lst].append('Хәйерле төн! (Доброй ночи)')
                        print('Хәйерле төн! (Доброй ночи)')
                bot.send_message(message.chat.id, random.choice(sample_answers[lst]))
                answer = 1
    if answer == 0:
        print('use send_answer_by_seq2seq')
        with tf.Session() as sess:
            sess, model, en_vocab, rev_fr_vocab = translate.start(sess)
            print("created sess")
            reply = translate.decode_for_bot(sess, model, en_vocab, rev_fr_vocab, text)
            reply = regUNK.sub('Ғәфү итегеҙ, мин аңламайым.',reply)
            bot.send_message(message.chat.id, reply)

# пустая главная страничка для проверки
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'OK!'


# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм
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