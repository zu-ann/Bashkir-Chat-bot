import telebot, re, conf, json, random, time, translate
import tensorflow as tf

sess = tf.Session()
sess, model, en_vocab, rev_fr_vocab = translate.start(sess)
print('created sess')
regUNK = re.compile('_UNK')

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
print('ready')

bot.remove_webhook()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
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
        reply = regUNK.sub('Ғәфү итегеҙ, мин аңламайым.', reply)
        bot.send_message(message.chat.id, reply)


if __name__ == '__main__':
    bot.polling(none_stop=True)