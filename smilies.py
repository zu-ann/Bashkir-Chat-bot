import urllib.request, re

page = urllib.request.urlopen('http://www.kody-smajlov-vkontakte.ru/')
text = page.read()
#fw = open('smiles.txt', 'w', encoding='UTF-8')
smile = re.compile('<td class="smile_code">(.+?)</td>')
res = smile.findall(str(text))
#for w in res:
    #fw.write(w + '\n')
#fw.close()
print(len(res))