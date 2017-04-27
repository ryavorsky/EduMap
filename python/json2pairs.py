#path = "../data/Direktor_shkoly/"
path = "../data/Nauka_i_shkola/"
json_file_name = "titles_and_abstracts.json"
top_file_name = "titles_and_abstracts_words_numbers.txt"

import json

excluded = ["автор", "без", "быть", "весь", "все", "вот", "где", "данный", "для", "даже", "его", "еще", "если",
            "или", "как", "какой", "когда", "который", "кто", "куда",
            "мой", "над", "наш", "она", "они", "оно", "при", "сам", "самый", "свой", "себя",
            "статья", "так", "также", "такой", "только", "тот", "уже", "чем", "что", "чтобы",
            "это", "этот"]

n_top = 100
top_words = []

res = dict() # final statistics for the pairs

# Get top numbered words from file
def get_top_words():
    global top_words
    top_file = open(path + top_file_name, "r", encoding="utf-8")
    data = top_file.readlines()[:n_top]
    for line in data:
        w = line.rstrip().split(" ")[1]
        top_words.append(w)
    print(top_words)

# order and glue two words
def word_pair(w1, w2):
    if w1 < w2 :
        return w1 + "_" + w2
    else:
        return w2 + "_" + w1

# get value from json
def lemma(d):
    analysis = d["analysis"]
    if len (analysis) == 0 :
        return ""
    else:
        return analysis[0]["lex"]

def main():

    get_top_words()

    # get the results of Mystem
    f = open(path + json_file_name, "r", encoding="utf-8")
    lines = f.readlines()

    # Calculate the number of pairs in each block
    current_line = 0
    while current_line < len(lines):
        title = lines[current_line]
        abstract = lines[current_line+1]
        current_line += 3

        title_words = [lemma(e) for e in json.loads(title)]
        abstract_words = [lemma(e) for e in json.loads(abstract)]
        words = list(set(title_words + abstract_words))  # join and remove duplicates
        print(current_line // 3, words)
        N = len(words)
        for i in range(N-1):
            for j in range(i+1,N):
                word1 = words[i]
                word2 = words[j]
                if (len(word1) > 2) and (len(word2) > 2):
                    if (word1 in top_words) or (word2 in top_words):
                        if (word1 not in excluded) and (word2 not in excluded):
                            pair = word_pair(word1, word2)
                            if pair in res:
                                res[pair] += 1
                            else:
                                res[pair] = 1

    print(top_words)
    res_list = [[k,v] for k,v in res.items()]
    res_list.sort(key=lambda tup: tup[1], reverse=True)
    print(res_list)

    res_file = open(path + "top_pairs.txt", "w", encoding="utf-8")
    for (k,v) in res_list:
        res_file.write(k + " " + str(v) + "\n")
    res_file.close()

main()