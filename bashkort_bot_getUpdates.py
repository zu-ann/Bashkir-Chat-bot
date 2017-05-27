import telebot, re, conf, json, random, time, phrases, TF_session
from telebot import types

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
print("Ready")

bot.remove_webhook()

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

def read_files():
    f1 = open('Sample_answers.json', 'r', encoding='UTF-8')
    f2 = open('Regex.json', 'r', encoding='UTF-8')
    f3 = open('Offensive_words.json', 'r', encoding='UTF-8')
    sample_answers = json.load(f1)
    regex = json.load(f2)
    offensive_words = json.load(f3)
    regex['offensive_words'] = offensive_words
    print("Opened files")
    f1.close()
    f2.close()
    f3.close()
    return sample_answers, regex

@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_sample_answers(message):
    write_logs(message.chat.id, message.text, message)
    print("Started send_sample_answers")
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
    write_logs('Bashkort_chatbot', answer_text, message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
