import telebot, re, conf, json, random, time, translate


bot = telebot.TeleBot(conf.TOKEN, threaded=False)

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
        bot.send_message(message.chat.id, translate.decode_for_bot(message.text))
    
              
if __name__ == '__main__':
    bot.polling(none_stop=True)
