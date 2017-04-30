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
    res = []

    f = open(fname, 'r', encoding='utf-8')
    lines = [line.strip() for line in  f.readlines()]

    title = ''
    authors = ''
    content = ''
    language_id = 0

    previous_line_type = "TITLE" # type of the previous line

    for line in lines:
        if len(line.rstrip()) > 2: # ignore small lines

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
                    abstract_and_keywords = content.replace("- ",'')
                    res.append([title,authors, abstract_and_keywords, languages[language_id], fname])
                    title, authors, content = '', '', ''
                    language_id = 1 - language_id
                    print("TITLE:", line)
                    title = line
                    previous_line_type = "TITLE"
                else:
                    print("CONTENT:", line)
                    content += " " + line
                    previous_line_type = "CONTENT"

    abstract_and_keywords = content.replace("- ", '')
    res.append([title, authors, abstract_and_keywords, languages[language_id], fname])
    return res

# main part
os.chdir('../data/Nauka_i_shkola/source/')
file_names = os.listdir()
print(os.getcwd(), os.listdir())

# Unite data from all files in one list
data = []
for file_name in os.listdir():
    data = data + text2table(file_name)

print(len(data), 'papers found')

# extract Russian part of the content
res_data = []
for block in data:
    if block[3]=="Rus":
        abstract_and_keywords = block[2].split("Ключевые слова: ")
        if len(abstract_and_keywords) < 2:
            abstract_and_keywords.append("")
        title = block[0].strip().upper()
        authors = block[1]
        abstract = abstract_and_keywords[0].replace("Аннотация.","")
        keywords = abstract_and_keywords[1].upper()
        volume = block[4].split(".")[0]
        year = volume.split("-")[0]
        data_unit = [title, authors, abstract, keywords, year, volume]
        res_data.append(data_unit)

# create the summary files
f_titles = open("../titles.txt", "w", encoding="utf-8")
f_authors = open("../authors.txt", "w", encoding="utf-8")
f_abstracts = open("../abstracts.txt", "w", encoding="utf-8")
f_titles_and_abstracts = open("../titles_and_abstracts.txt", "w", encoding="utf-8")

for block in res_data:
    f_titles.write(block[5] + ": " + block[0] + "\n")
    f_authors.write(block[5] + ": " + block[1] + "\n")
    f_abstracts.write(block[5] + ": " + block[2] + "\t" + block[3] + "\n")
    f_titles_and_abstracts.write(block[4] + "\t" + block[5] + "\n" + block[0] + "\n" + block[2] + "\t" + block[3] + "\n\n")

f_titles.close()
f_authors.close()
f_abstracts.close()
f_titles_and_abstracts.close()
