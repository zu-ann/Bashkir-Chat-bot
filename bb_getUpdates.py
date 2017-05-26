import telebot, re, conf, json, random, time, TF_session

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
print('ready')

bot.remove_webhook()

def write_logs(id, text):
    with open('logs.txt','a',encoding='utf') as f:
        f.write(str(id) + ':\t' + text + '\n')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    write_logs(message.chat.id, message.text)
    print("started send_welcome")
    start = 'Cәләм! Мин башҡорт телендә һөйләшә белгән беренсе бот, әйҙә аралашайыҡ!'
    bot.send_message(message.chat.id, start)
    write_logs('Bashkort_chatbot', start)

@bot.message_handler(commands=['help'])
def send_help(message):
    write_logs(message.chat.id, message.text)
    print("started send_help")
    help = 'This bot can carry on a dialogue using the Bashkir language.\n Supported commands:\n /start - start the conversation\n /help - about the bot\n /mark - give a mark to the quality of the bot\'s answers\n\n If you want to get more information about this bot – please visit https://github.com/zu-ann/Bashkort_chatbot'
    bot.send_message(message.chat.id, help)
    write_logs('Bashkort_chatbot', help)

@bot.message_handler(commands=['mark'])
def get_mark(message):
    write_logs(message.chat.id, message.text)
    markup = types.ReplyKeyboardMarkup(row_width=3,one_time_keyboard=1)
    itembtn1 = types.KeyboardButton('👎')
    itembtn2 = types.KeyboardButton('😐')
    itembtn3 = types.KeyboardButton('👍')
    markup.add(itembtn1, itembtn2, itembtn3)
    text = "Please choose the image that best describes your opinion of how appropriate the bot's answers are:"
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(regexp = '[👎😐👍]')
def read_marks(message):
    text = message.text
    if text == '👎':
        mark = '0'
    elif text == '🙂':
        mark = 1
    else:
        mark = 2
    write_logs(message.chat.id, str(mark))

@bot.message_handler(regexp ='[a-gi-uwxzA-GI-UWXZ]+')
def other_language(message):
    write_logs(message.chat.id, message.text)
    print("other language")
    bot.send_message(message.chat.id, 'Sorry, please speak Bashkir.')
    write_logs('Bashkort_chatbot', 'Sorry, please speak Bashkir.')

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
    write_logs(message.chat.id, message.text)
    print("started send_sample_answers")
    sample_answers, regex = read_files()
    text = message.text
    answer = 0
    for lst in regex:
        for elem in regex[lst]:
            res = re.search(elem, text)
            if res:
                if lst == 'formal_greeting':
                    hour = int(time.strftime('%H', time.gmtime(message.date))) + 3
                    if 4 <= hour < 12:
                        sample_answers[lst].append('Хәйерле иртә!')
                        print('Хәйерле иртә! (доброе утро)')
                    if 12 <= hour <= 16:
                        sample_answers[lst].append('Хәйерле көн!')
                        print('Хәйерле көн! (добрый день)')
                    if 16 < hour <= 22:
                        sample_answers[lst].append('Хәйерле кис!')
                        print('Хәйерле кис! (добрый вечер)')
                    if hour > 22 or hour < 4:
                        sample_answers[lst].append('Хәйерле төн!')
                        print('Хәйерле төн! (Доброй ночи)')
                if not lst.endswith('greeting') and not lst.endswith('goodbye'):
                    key = lst + '_answer'
                else:
                    key = lst
                answer_text = random.choice(sample_answers[key])
                answer = 1
    if answer == 0:
        answer_text = TF_session.answer_by_seq2seq(text)
    bot.send_message(message.chat.id, answer_text)
    write_logs('Bashkort_chatbot', answer_text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
