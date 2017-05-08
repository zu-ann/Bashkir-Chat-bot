import flask, telebot, re, conf, json, random, time, translate

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)

# удаляем предыдущие вебхуки, если они были
bot.remove_webhook()

# ставим новый вебхук = Слышь, если кто мне напишет, стукни сюда — url
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

# этот обработчик запускает функцию send_welcome, когда пользователь отправляет команды /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Это бот на башкирском.")

@bot.message_handler(content_types=['text'])
def send_sample_answers(message):
    message.text = text
    f1 = open("Sample_answers.json")
    sample_answers = json.load(f1)
    for list in sample_answers:
        for elem in sample_answers[list]:
            res = re.search(elem,text)
            if res:
                if not list.endswith('greeting') and not list.endswith('goodbye'):
                    list += '_answer'
                elif list == 'formal_greeting':
                    hour = time.strftime('%H',time.gmtime(message.date))
                    if 4 <= hour < 12: #'Хәйерле иртә! (доброе утро), Хәйерле көн! (добрый день), Хәйерле кис! (добрый вечер), Хәйерле төн! (Доброй ночи),
                        sample_answers[list].append('Хәйерле иртә! (доброе утро)')
                    if 12 <= hour <= 16:
                        sample_answers[list].append('Хәйерле көн! (добрый день)')
                    if 16 < hour <= 22:
                        sample_answers[list].append('Хәйерле кис! (добрый вечер)')
                    if hour > 22 or hour < 4:
                        sample_answers[list].append('Хәйерле төн! (Доброй ночи)')
                bot.send_message(message.chat.id, random.choice(sample_answers[list]))

@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_answer_by_seq2seq(message):
    bot.send_message(message.chat.id, translate.decode_for_bot(message.text))

# пустая главная страничка для проверки
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


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
