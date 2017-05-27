import json, os, re, random, math

path = 'C:\\Users\\zu_ann\\Bashkort_chatbot_all_files\\bak_vk_corpus'

def select_dialogs(path):
    q = []
    a = []
    for root, dirs, files in os.walk(path):
        for dr in dirs:
            fls = os.listdir(path + '\\' + dr)
            for f in fls:
                files.append(dr + '\\' + f) # в массив с файлами добавляем файлы из папок
        for fl in files:
            if fl.endswith('.json'):
                fr = open(root + '\\' + fl, 'r', encoding='UTF-8')
                data = json.load(fr)
                fr.close()
                data = list(data.values())
                for d in data:
                    for key in d:
                        if key == 'posts':
                            posts = d[key]
                            for num in sorted(posts):
                                post = posts[num]
                                if post['comments']:
                                    dt = {}
                                    comments = post['comments']
                                    for num2 in sorted(comments):
                                        comment = comments[num2]
                                        date_time_comm = comment['date']
                                        text_comm = comment['text']
                                        dt[date_time_comm] = text_comm
                                    try:
                                        date_time_p = post['date']
                                        text = post['text']
                                        dt[date_time_p] = text
                                    except:
                                        continue
                                    sort_comments(dt, q, a)
                                else:
                                    text = post['text']
                                    split_posts(clean_dialogs(text), q, a)
    print('the number of questions: {}'.format(len(q)))
    print('the number of answers: {}'.format(len(a)))
    create_files(q, a)

def sort_comments(dt, q, a):
    comm_sort = []
    for date_time in sorted(dt):
        comm_sort.append(clean_dialogs(dt[date_time]))
    for k in range(len(comm_sort) - 1):
        q.append(comm_sort[k] + '\n')
    for k in range(1, len(comm_sort)):
        a.append(comm_sort[k] + '\n')

def clean_dialogs(text):
    text = text.lower()
    for sym in text:
        if (ord(sym) > 1327 and ord(sym) not in range(8192, 8303)):
            text = text.replace(sym, '')
    text = text.replace('\n',' ')
    text = text.replace('\r', ' ')
    text = text.replace('<br>', ' ')
    url = re.compile('(https?|www)[0-9a-z/.\-%=?:&_]+')
    pers = re.compile('\[.*?\]')
    numb = re.compile('[0-9]+')
    text = re.sub(url, '<url>', text)
    text = re.sub(pers, '<reference>', text)
    text = re.sub(numb, '<number>', text)
    return text

def split_posts(text, q, a):
    eos = re.compile('([\.!?()]+)')
    res = eos.split(text)
    sentences = []
    for k in range(1, len(res), 2):
        res[k - 1] += res[k]
        sentences.append(res[k - 1])
        if k + 1 == len(res) - 1 and res[k + 1] != '':
            sentences.append(res[k + 1])
    questions = ''
    answers = ''
    if len(sentences) > 1:
        if len(sentences) % 2 == 0:
            for k in range(len(sentences) // 2):
                questions += str(sentences[k])
            for k in range(len(sentences) // 2, len(sentences)):
                answers += str(sentences[k])
        else:
            for k in range(len(sentences) // 2 + 1):
                questions += str(sentences[k])
            for k in range(len(sentences) // 2 + 1, len(sentences)):
                answers += str(sentences[k])
        q.append(questions + '\n')
        a.append(answers + '\n')

def create_files(q,a):
    test_size = math.trunc(len(q) * 0.3)
    train_q = open('train.en', 'w', encoding='UTF-8')
    train_a = open('train.fr', 'w', encoding='UTF-8')
    test_q = open('test.en', 'w', encoding='UTF-8')
    test_a = open('test.fr', 'w', encoding='UTF-8')
    test_ids = random.sample([i for i in range(len(q))], test_size)
    for i in range(len(q)):
        if i in test_ids:
            test_q.write(q[i])
            test_a.write(a[i])
        else:
            train_q.write(q[i])
            train_a.write(a[i])
        if i % 10000 == 0:
            print('written {} lines'.format(i))
    train_q.close()
    train_a.close()
    test_q.close()
    test_a.close()

if __name__ == '__main__':
    select_dialogs(path)