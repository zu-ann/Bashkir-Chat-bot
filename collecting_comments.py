import json, os, re


def select_dialogs():
    fw = open('bash_data.tsv', 'w', encoding='UTF-8')
    i = 1
    path = 'C:\\Users\\zu_ann\\Documents\\Linguistics\\bak_vk_corpus'
    for root, dirs, files in os.walk(path):
        for dr in dirs:
            fls = os.listdir(dr)
            for f in fls:
                files.append(dr + '\\' + f)
        for fl in files:
            if fl.endswith('.json'):
                fr = open(root + '\\' + fl, 'r', encoding='UTF-8')
                data = json.load(fr)
                fr.close()
                data = list(data.values())
                dt = {}
                for d in data:
                    for key in d:
                        if key == 'posts': 
                            posts = d[key]
                            for num in sorted(posts):
                                post = posts[num]
                                try:
                                    date_time = post['date']
                                    text = post['text']
                                    dt[date_time] = text
                                except:
                                    continue
                                if post['comments'] != '{}':
                                    comments = post['comments']
                                    for num2 in sorted(comments):
                                        comment = comments[num2]
                                        date_time = comment['date']
                                        text = comment['text']
                                        dt[date_time] = text
                sort_dialogs(dt,i,fw)
    fw.close()

def sort_dialogs(dt,i,fw):
    for date_time in sorted(dt):
        fw.write(str(i) + '\t' + date_time + '\t' + clean_dialogs(dt[date_time]) + '\n')
        print(i)
        i += 1

def clean_dialogs(text):
    f = open('smilies.txt','r',encoding = 'utf-8')
    text = text.replace('\n',' ')
    text = text.replace('\r', ' ')
    text = text.replace('<br>', ' ')
    url = re.compile('(https?|www)[0-9a-z/.\-%=?:&_]+')
    pers = re.compile('\[.*?\]')
    numb = re.compile('[0-9]+')
    hashtag = re.compile('#.*?( |\n|,)')
    for smiley in f:
        if smiley in text:
            text = text.replace(smiley, '<smiley>')
            print(text)
    text = re.sub(url, '<url>', text)
    text = re.sub(pers, '<reference>', text)
    text = re.sub(numb, '<number>', text)
    #text = re.sub(hashtag, '<hashtag>\1', text)
    return text

if __name__ == '__main__':
    select_dialogs()
