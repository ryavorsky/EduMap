file_name = "dir_shk_words"
excluded = ["без", "быть", "все", "вот", "где", "для", "даже", "его", "еще", "или", "как", "какой", "который", "кто", "куда",
            "мой", "над", "наш", "она", "они", "оно", "при", "сам", "свой", "так", "также", "такой", "только", "тот", "уже", "что", "чтобы",
            "это", "этот"]

def step1_clean():

    f_in = open(file_name + ".txt", "r", encoding="utf-8")

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

    f_out = open(file_name + "_clean.txt", "w", encoding="utf-8")
    for (k,l) in res_list_numbers:
        f_out.write(str(k) + " " + l + "\n")
    f_out.close()


step1_clean()