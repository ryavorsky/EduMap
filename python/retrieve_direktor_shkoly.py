from urllib.request import urlopen

f = open("../data/DirektorShkoly-urls.txt","r",encoding="utf-8")
lines = [line.rstrip() for line in f.readlines()]

for line in lines:
    data = line.split(",")
    print(data)
    issue_no = data[0]
    year = data[1]
    date = data[2]
    url = data[3]
    file_name = year + "_" + issue_no + ".txt"
    f_out = open("../data/Direktor_shkoly/html/" + file_name, "wb")
    html = urlopen(url)
    content = html.read()
    print(content)
    f_out.write(content)
    f_out.close()

f.close()