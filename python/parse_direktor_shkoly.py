import os
import sys

os.chdir('../data/Direktor_Shkoly/html/')

file_names = os.listdir()
print(os.getcwd(), os.listdir())

for file_name in file_names:
    f_in = open(file_name, "r", encoding="cp1251")
    source_text = f_in.read()
    source_text = source_text.split('alt="Содержание номера"></p>')[1]
    source_text = source_text.split('</td>')[0]
    source_text = source_text.replace('\t\t<p class="main_tagline"><b>',"Authors:")
    source_text = source_text.replace("<br></b>", "\nAbstract:")
    source_text = source_text.replace('\t\t<p class="main" style="text-align: left"><b>', "\nTitle:")
    source_text = source_text.replace("</b></p>", "")
    #source_text = source_text.replace("</p>", "\n")

    lines = source_text.split("\n")

    f_out = open("../content/" + file_name, "w", encoding="utf-8")
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
                block = [title, authors, abstract]
                f_out.write("\n".join(block) + "\n\n")
                last_line_type = "Space"

        elif last_line_type == "Authors":
            if line.find("Abstract:") > -1:
                abstract = line[9:]
                last_line_type = "Abstract"
                pos_b = abstract.find("<")
                if pos_b > -1:
                    abstract = abstract.split("<")[0]
                    block = [title, authors, abstract]
                    f_out.write("\n".join(block) + "\n\n")
                    last_line_type = "Space"
            else:
                abstract = ""
                block = [title, authors, abstract]
                f_out.write("\n".join(block) + "\n\n")
                last_line_type = "Space"

        elif last_line_type == "Abstract":
            abstract += line
            pos_b = abstract.find("<")
            if pos_b > -1:
                abstract = abstract.split("<")[0]
                block = [title, authors, abstract]
                f_out.write("\n".join(block) + "\n\n")
                last_line_type = "Space"

    f_out.close()

    f_in.close()
