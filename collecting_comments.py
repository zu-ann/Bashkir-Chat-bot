import json, os, re


def select_dialogs():
    fw = open('bash_data.tsv', 'w', encoding='UTF-8')
    path = 'C:\\Users\\zu_ann\\Documents\\Linguistics\\bak_vk_corpus'
    for root, dirs, files in os.walk(path):
        i = 1
        for dr in dirs:
            fls = os.listdir(dr)
            for f in fls:
                files.append(dr + '\\' +f)
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
                                for key2 in post:
                                    if key2 == 'text':
                                        text = post[key2]
                                        fw.write(str(i) + '\t' + clean_dialogs(text) + '\n')
                                        i += 1
    fw.close()

def clean_dialogs(text):
    text = text.replace('\n',' ')
    text = text.replace('\r', ' ')
    text = text.replace('<br>', ' ')
    url = re.compile('(https?|www)[0-9a-z/.\-%=?:&_]+')
    pers = re.compile('\[.*?\]')
    numb = re.compile('[0-9]{5,}')
    text = re.sub(url, '', text)
    text = re.sub(pers, '', text)
    text = re.sub(numb, '', text)
    return text

if __name__ == '__main__':
    select_dialogs()