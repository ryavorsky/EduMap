#path = "../data/Direktor_shkoly/"
path = "../data/Nauka_i_shkola/"
file_name = "titles_and_abstracts_words.txt"

excluded = ["автор", "без", "быть", "весь", "все", "вот", "где", "данный", "для", "даже", "его", "еще", "если",
            "или", "как", "какой", "когда", "который", "кто", "куда",
            "мой", "над", "наш", "она", "они", "оно", "при", "сам", "самый", "свой", "себя",
            "статья", "так", "также", "такой", "только", "тот", "уже", "чем", "что", "чтобы",
            "это", "этот"]

def word_count():

    f_in = open(path + file_name, "r", encoding="utf-8")

    data = f_in.readlines()
    data = [line.rstrip().replace("?","").split("|")[0] for line in data]
    data.sort()

    res_list = []

    for line in data:
        if (len(line) > 2) and (line not in excluded):
            res_list.append(line)

    res_list_numbers = []
    prev_line = res_list[0]
    k = 0
    for line in res_list:
        if line == prev_line:
            k += 1
        else:
            res_list_numbers.append([k, prev_line])
            k = 1
        prev_line = line
    res_list_numbers.append([k, prev_line])
    res_list_numbers.sort(key=lambda tup: tup[0], reverse=True)

    file_res_name = path + file_name.split(".")[0] + "_numbers.txt"
    f_out = open(file_res_name, "w", encoding="utf-8")
    for (k,l) in res_list_numbers:
        f_out.write(str(k) + " " + l + "\n")
    f_out.close()


word_count()