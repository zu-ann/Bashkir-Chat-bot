import json, os, re, random, math


def select_dialogs():
    q = []
    a = []
    i = 1
    path = 'C:\\Users\\zu_ann\\Documents\\Linguistics\\bak_vk_corpus'
    for root, dirs, files in os.walk(path):
        for dr in dirs:
            fls = os.listdir(dr)
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
                                        #print(dt)
                                    except:
                                        continue
                                    sort_comments(dt, i, q, a)
                                else:
                                    date_time_p = post['date']
                                    text = post['text']
                                    split_posts(clean_dialogs(text), date_time_p, i, q, a)
    #print(q)
    print(len(q))
    #print(a)
    print(len(a))
    create_files(q, a)

def sort_comments(dt,i,q,a):
    comm_sort = []
    for date_time in sorted(dt):
        comm_sort.append(date_time + '\t' + clean_dialogs(dt[date_time]))
    for k in range(len(comm_sort) - 1):
        q.append(str(i) + '\t' + comm_sort[k] + '\n')
        i += 1
    for k in range(1, len(comm_sort)):
        a.append(str(i) + '\t' + comm_sort[k] + '\n')
        i += 1
    print(i)

def clean_dialogs(text):
    text = text.lower()
    text = text.replace('\n',' ')
    text = text.replace('\r', ' ')
    text = text.replace('<br>', ' ')
    url = re.compile('(https?|www)[0-9a-z/.\-%=?:&_]+') #( .*?\.([Cc][oO][Mm]|[Oo][rR][Gg]|[rR][uU]))
    pers = re.compile('\[.*?\]')
    numb = re.compile('[0-9]+')
    text = re.sub(url, '<url>', text)
    text = re.sub(pers, '<reference>', text)
    text = re.sub(numb, '<number>', text)
    return text

def split_posts(text, date_time_p, i, q, a):
    eos = re.compile('([\.!?()]+)')
    # print(text)
    res = eos.split(text)
    sentences = []
    for k in range(1, len(res), 2):
        res[k - 1] += res[k]
        sentences.append(res[k - 1])
        if k + 1 == len(res) - 1 and res[k + 1] != '':
            sentences.append(res[k + 1])
    # print(sentences)
    questions = ''
    answers = ''
    # print(len(sentences))
    if len(sentences) > 1:
        if len(sentences) % 2 == 0:
            for k in range(len(sentences) // 2):
                questions += str(sentences[k])
                # print(questions)
            for k in range(len(sentences) // 2, len(sentences)):
                answers += str(sentences[k])
                # print(answers)
        else:
            for k in range(len(sentences) // 2 + 1):
                questions += str(sentences[k])
                # print(questions)
            for k in range(len(sentences) // 2 + 1, len(sentences)):
                answers += str(sentences[k])
                # print(answers)
        q.append(str(i) + '\t' + date_time_p + '\t' + questions + '\n')
        a.append(str(i) + '\t' + date_time_p + '\t' + answers + '\n')
        print(i)
        i += 1

def create_files(q,a):
    test_size = math.trunc(len(q) * 0.3)
    print(test_size)
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
            print('>> written {} lines'.format(i))
    train_q.close()
    train_a.close()
    test_q.close()
    test_a.close()

if __name__ == '__main__':
    select_dialogs()