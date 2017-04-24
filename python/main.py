import os

languages = ["Rus", "Eng"]

def is_mainly_upper(line):
    line0 = line.replace(".","").replace(" ","")
    line1 = line0.upper()
    L = len(line0)
    if L < 5 :
        return False
    else:
        if L>30 :
            L = 30
        upper = 0.0
        for i in range(L):
            if (line0[i] == line1[i]):
                upper += 1.0
        return (upper / L > 0.7)


# convert raw text file into the four columns table (title, author, content, language)
def text2table(fname):
    res = list()

    f = open(fname, 'r', encoding='utf-8')
    lines = [line.strip() for line in  f.readlines()]

    title = ''
    authors = ''
    content = ''
    language_id = 0

    previous_line_type = "TITLE" # type of the previous line

    for line in lines:
        if len(line.rstrip()) > 2:

            # after TITLE could be TITLE or AUTHORS
            if previous_line_type == "TITLE":
                if is_mainly_upper(line):
                    print("TITLE:", line)
                    title += " " + line
                    previous_line_type == "TITLE"
                else:
                    print("AUTHORS:", line)
                    authors = line
                    previous_line_type = "AUTHORS"

            # after AUTHORS always is CONTENT
            elif (previous_line_type == "AUTHORS"):
                print("CONTENT:", line)
                content += line
                previous_line_type = "CONTENT"

            # after CONTENT could be CONTENT or new AUTHORS
            elif previous_line_type == "CONTENT" :
                if is_mainly_upper(line):
                    # the previous block has finished
                    res.append([title,authors,content.replace("- ",''), languages[language_id], fname])
                    title, authors, content = '', '', ''
                    language_id = 1 - language_id
                    print("TITLE:", line)
                    title = line
                    previous_line_type = "TITLE"
                else:
                    print("CONTENT:", line)
                    content += " " + line
                    previous_line_type = "CONTENT"
    res.append([title, authors, content.replace("- ", ''), languages[language_id], fname])
    return res


os.chdir('../data/Nauka_i_shkola/')
file_names = os.listdir()
print('Hello', os.getcwd(), os.listdir())

data = []
for file_name in os.listdir():
    data = data + text2table(file_name)

print(len(data), 'papers found')

res_file = open('../data.txt','w', encoding='utf-8')
for block in data:
    if block[3]=="Rus":
        #print(block)
        content = block[2].split("Ключевые слова: ")
        if len(content) < 2:
            content.append("---")
        res_file.write('\n' + block[4] + ' ' + block[3] + ':\n' + content[1].upper() + '\n' + content[0] + '\n')
res_file.close()
