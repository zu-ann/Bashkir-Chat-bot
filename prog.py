import json, os, re


def select_dialogs():
    fw_q = open('bash_data_q.tsv', 'a', encoding='UTF-8')
    fw_a = open('bash_data_a.tsv', 'a', encoding='UTF-8')
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
                                if post['comments'] != '{}':
                                    dt = {}
                                    try:
                                        date_time_p = post['date']
                                        text = post['text']
                                        dt[date_time_p] = text
                                    except:
                                        continue
                                    comments = post['comments']
                                    for num2 in sorted(comments):
                                        comment = comments[num2]
                                        date_time_comm = comment['date']
                                        text_comm = comment['text']
                                        dt[date_time_comm] = text_comm
                                    sort_comments(dt, i, fw_q, fw_a)
                                else:
                                    date_time_p = post['date']
                                    text = post['text']
                                    split_posts(clean_dialogs(text), date_time_p, i, fw_q, fw_a)
    fw_q.close()
    fw_a.close()

def sort_comments(dt, i, fw_q, fw_a):
    comm_sort = []
    for date_time in sorted(dt):
        comm_sort.append(date_time + '\t' + clean_dialogs(dt[date_time]))
    for k in range(0, len(comm_sort) - 1):
        fw_q.write(str(i) + '\t' + comm_sort[k] + '\n')
        i += 1
    for k in range(1, len(comm_sort)):
        fw_a.write(str(i) + '\t' + comm_sort[k] + '\n')
        i += 1
    print(i)

def clean_dialogs(text):
    text = text.replace('\n',' ')
    text = text.replace('\r', ' ')
    text = text.replace('<br>', ' ')
    url = re.compile('(https?|www|(.+?\.([Cc][oO][Mm]|[Oo][rR][Gg]|[rR][uU])))[0-9a-z/.\-%=?:&_]*')
    pers = re.compile('\[.*?\]')
    numb = re.compile('[0-9]+')
    text = re.sub(url, '<url>', text)
    text = re.sub(pers, '<reference>', text)
    text = re.sub(numb, '<number>', text)
    return text

def split_posts(i,text, date_time_p,fw_q,fw_a):
    sentences = text.split('.' or '!' or '?')
    questions = ''
    answers = ''
    if len(sentences) % 2 == 0:
        for i in range(0, len(sentences)/2):
            questions += str(sentences[i])
        for i in range(len(sentences)/2 + 1,):
            answers += str(sentences[i])
    else:
        for i in range(0, len(sentences)/2 + 1):
            questions += str(sentences[i])
        for i in range(len(sentences)/2 + 2,):
            answers += str(sentences[i])
    fw_q.write(str(i) + '\t' + date_time_p + '\t' + questions + '\n')
    fw_a.write(str(i) + '\t' + date_time_p + '\t' + answers + '\n')
    print(i)
    i += 1

if __name__ == '__main__':
    select_dialogs()
