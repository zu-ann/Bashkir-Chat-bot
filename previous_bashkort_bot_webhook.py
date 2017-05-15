# -*- coding: utf-8 -*-
import telebot, os, re, conf, json, random, time, translate
from flask import Flask, request
import tensorflow as tf

WEBHOOK_HOST = 'bashkort-bot.herokuapp.com'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '162.243.19.215'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = 'webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'  # Path to the ssl private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (conf.TOKEN)

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, 'r'))

bot = telebot.TeleBot(conf.TOKEN, threaded=False)

app = Flask(__name__)

sess = tf.Session()
sess, model, en_vocab, rev_fr_vocab = translate.start(sess)
print('created sess')
regUNK = re.compile('_UNK')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Это бот на башкирском.")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_sample_answers(message):
    text = message.text
    answer = 0
    f1 = open('Sample_answers.json','r',encoding = 'UTF-8')
    f2 = open('regex.json','r',encoding = 'UTF-8')
    sample_answers = json.load(f1)
    regex = json.load(f2)
    f1.close()
    f2.close()
    for lst in regex:
        for elem in regex[lst]:
            res = re.search(elem,text)
            if res:
                if not lst.endswith('greeting') and not lst.endswith('goodbye'):
                    lst += '_answer'
                elif lst == 'formal_greeting':
                    hour = int(time.strftime('%H',time.gmtime(message.date))) + 3
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
        reply = translate.decode_for_bot(sess, model, en_vocab, rev_fr_vocab, text)
        reply = regUNK.sub('Ғәфү итегеҙ, мин аңламайым.',reply)
        bot.send_message(message.chat.id, reply)
                   
app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
        debug=True)
