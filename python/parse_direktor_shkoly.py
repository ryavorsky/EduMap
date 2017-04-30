import os
import sys

os.chdir('../data/Direktor_Shkoly/html/')

file_names = os.listdir()
print(os.getcwd(), os.listdir())

res_data = []

for file_name in file_names:

    f_in = open(file_name, "r", encoding="cp1251")
    source_text = f_in.read()
    f_in.close()

    year = file_name.split(".")[0].split("_")[0]
    issue = file_name.split(".")[0].split("_")[1]

    source_text = source_text.split('alt="Содержание номера"></p>')[1]
    source_text = source_text.split('</td>')[0]
    source_text = source_text.replace('\t\t<p class="main_tagline"><b>',"Authors:")
    source_text = source_text.replace("<br></b>", "\nAbstract:")
    source_text = source_text.replace('\t\t<p class="main" style="text-align: left"><b>', "\nTitle:")
    source_text = source_text.replace("</b></p>", "")
    #source_text = source_text.replace("</p>", "\n")

    lines = source_text.split("\n")

    #f_out.write(source_text)
    #f_out.close()
    #sys.exit("Done so far")

    last_line_type = "Space"

    for line in lines:
        #f_out.write(last_line_type + "###" + line + "\n")
        if last_line_type == "Space" :
            if line.find("Title:") > -1 :
                title = line[6:].upper()
                if title.find("<") == 0:
                    title = title.split(">")[1]
                    title = title.split("<")[0]
                last_line_type = "Title"

        elif last_line_type == "Title" :
            if line.find("Authors:") > -1:
                authors = line[8:]
                last_line_type = "Authors"
            else:
                authors = ""
                abstract = ""
                res_data.append([title, authors, abstract, year, issue])
                last_line_type = "Space"

        elif last_line_type == "Authors":
            if line.find("Abstract:") > -1:
                abstract = line[9:]
                last_line_type = "Abstract"
                pos_b = abstract.find("<")
                if pos_b > -1:
                    abstract = abstract.split("<")[0]
                    res_data.append([title, authors, abstract, year, issue])
                    last_line_type = "Space"
            else:
                abstract = ""
                res_data.append([title, authors, abstract, year, issue])
                last_line_type = "Space"

        elif last_line_type == "Abstract":
            abstract += line
            pos_b = abstract.find("<")
            if pos_b > -1:
                abstract = abstract.split("<")[0]
                res_data.append([title, authors, abstract, year, issue])
                last_line_type = "Space"

f_titles = open("../titles.txt", "w", encoding="utf-8")
f_authors = open("../authors.txt", "w", encoding="utf-8")
f_abstracts = open("../abstracts.txt", "w", encoding="utf-8")
f_titles_and_abstracts = open("../titles_and_abstracts.txt", "w", encoding="utf-8")

for block in res_data:
    if len(block[2]) > 0:
        f_titles.write(block[4] + ":" + block[0] + "\n")
        f_authors.write(block[4] + ":" + block[1] + "\n")
        f_abstracts.write(block[4] + ":" + block[2] + "\n")
        f_titles_and_abstracts.write(block[3] + "\t" + block[4] + "\n" + block[0] + "\n" + block[2] + "\n\n")

f_titles.close()
f_authors.close()
f_abstracts.close()
f_titles_and_abstracts.close()

