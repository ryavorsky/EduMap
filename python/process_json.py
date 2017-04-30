path = "../data/Direktor_shkoly/"
#path = "../data/Nauka_i_shkola/"
json_file_name = "titles_and_abstracts.json"
#top_file_name = "titles_and_abstracts_words_numbers.txt"

import json

excluded = ["автор", "без", "быть", "ваш", "ведь", "весь", "все", "вот", "вряд", "где", "данный", "для", "даже",
            "его", "еще", "если",
            "зато", "зачастую", "или", "как", "каков", "какой", "когда", "который", "кто", "кто-то", "куда",
            "между", "многие", "мой", "над", "наш", "нет", "обо", "однако", "она", "они", "оно", "очень",
            "передо", "пока", "после", "почему", "почти", "при", "про",
            "сам", "самый", "свой", "себя", "сей", "сейчас", "среди",
            "статья", "так", "также", "такой", "тогда", "только", "тот", "уже", "хотя", "чем", "через", "что", "что-то", "чтобы",
            "это", "этот"]


# order and glue two words
def word_pair(w1, w2):
    if w1 < w2:
        return w1 + "_" + w2
    else:
        return w2 + "_" + w1


# get normalized word from json
def lemma(d):
    if "analysis" not in d:
        return ""
    else:
        analysis = d["analysis"]
        if len (analysis) == 0 :
            return ""
        else:
            return analysis[0]["lex"]


# get data from json file
def parse_json(fname):
    res = [] # will be list of pairs [year, list of words]

    f = open(path + json_file_name, "r", encoding="utf-8")
    lines = f.readlines()

    # Calculate the number of pairs in each block
    current_line = 0
    while current_line < len(lines):

        year = json.loads(lines[current_line])[0]["text"]
        title = lines[current_line+1]
        abstract = lines[current_line+2]
        current_line += 4

        title_words = [lemma(e) for e in json.loads(title)]
        abstract_words = [lemma(e) for e in json.loads(abstract)]
        words_set = set(title_words + abstract_words)
        words_list = []
        for w in words_set:
            if (len(w)>2) and (w not in excluded):
                words_list.append(w)
        res.append([year, words_list])
        #print(current_line // 4, [year,words_list])

    return res


def count_pairs(data):
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


data = parse_json(path + json_file_name)

all_words = set()
for block in data:
    all_words = all_words.union(set(block[1]))

print(len(data), "papers")
print (len(all_words), "words\n")

word_count = dict()
for w in all_words:
    word_count[w] = {"all":0, "2010":0, "2011":0, "2012":0, "2013":0, "2014":0, "2015":0, "2016":0, "2017":0}

for block in data:
    for w in block[1]:
        word_count[w]["all"] += 1
        word_count[w][block[0]] +=1

top_words_cont = dict()
for w in word_count:
    if word_count[w]["all"] > 15:
        if (word_count[w]["2015"] + word_count[w]["2016"] + word_count[w]["2017"]) * 2 > word_count[w]["all"]:
            top_words_cont[w] = word_count[w]

top_words = top_words_cont.keys()
print(len(top_words_cont), top_words_cont)

low_words_cont = dict()
for w in word_count:
    if word_count[w]["all"] > 20:
        if (word_count[w]["2010"] + word_count[w]["2011"] + word_count[w]["2012"]) * 2 > word_count[w]["all"]:
            low_words_cont[w] = word_count[w]

low_words = low_words_cont.keys()
print(len(low_words_cont), low_words_cont)