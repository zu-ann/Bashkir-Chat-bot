import os,json,re

fw = open('bash_com.tsv', 'w', encoding='UTF-8')
i = 1
path = 'C:\\Users\\zu_ann\\Documents\\Linguistics\\bak_vk_corpus'
for root, dirs, files in os.walk(path):
    t = re.compile('2013-10-10 08:45:32')
    for dr in dirs:
        fls = os.listdir(dr)
        for f in fls:
            files.append(dr + '\\' + f)
    for fl in files:
        if fl.endswith('.json'):
            fr = open(root + '\\' + fl, 'r', encoding='UTF-8')
            data = json.load(fr)
            fr.close()
            a = t.search(str(data))
            if a:
                print(fl)
fw.close() 
