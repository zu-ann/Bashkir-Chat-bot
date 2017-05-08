import telebot, re, conf, json, random, time, translate #flask,

#WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
#WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)

# удаляем предыдущие вебхуки, если они были
#bot.remove_webhook()

# ставим новый вебхук = Слышь, если кто мне напишет, стукни сюда — url
#bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

#app = flask.Flask(__name__)

# этот обработчик запускает функцию send_welcome, когда пользователь отправляет команды /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Это бот на башкирском.")

@bot.message_handler(content_types=['text'])
def send_sample_answers(message):
    text = message.text
    f1 = open('Sample_answers.json','r',encoding = 'UTF-8')
    f2 = open('regex.json','r',encoding = 'UTF-8')
    sample_answers = json.load(f1)
    regex = json.load(f2)
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

@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_answer_by_seq2seq(message):
   bot.send_message(message.chat.id, translate.decode_for_bot(message.text))

# пустая главная страничка для проверки
#@app.route('/', methods=['GET', 'HEAD'])
#def index():
#    return 'ok'


# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм
#@app.route(WEBHOOK_URL_PATH, methods=['POST'])
#def webhook():
#    if flask.request.headers.get('content-type') == 'application/json':
#        json_string = flask.request.get_data().decode('utf-8')
#        update = telebot.types.Update.de_json(json_string)
#        bot.process_new_updates([update])
#        return ''
#    else:
#        flask.abort(403)

if __name__ == '__main__':
    bot.polling(none_stop=True)