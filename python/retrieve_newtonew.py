from urllib.request import urlopen

f = open("../data/Newtonew/urllist.txt","r",encoding="utf-8")
lines = [line.rstrip() for line in f.readlines()]

for url in lines:
    file_name = url.split("/")[-1] + ".txt"
    f_out = open("../data/Newtonew/download/" + file_name, "wb")
    html = urlopen(url)
    content = html.read()
    print(content)
    f_out.write(content)
    f_out.close()

f.close()
