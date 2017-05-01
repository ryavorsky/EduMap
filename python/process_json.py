#path = "../data/Direktor_shkoly/"
#years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
path = "../data/Nauka_i_shkola/"
years = [2013, 2014, 2015, 2016, 2017]
json_file_name = "titles_and_abstracts.json"

trend_threshold = 1.3

import json

excluded = ["автор", "без", "быть", "ваш", "ведь", "весь", "все", "вот", "вряд", "где", "данный", "для", "даже",
            "его", "еще", "если",
            "зато", "зачастую", "или", "именно", "как", "каков", "какой", "когда", "который", "кто", "кто-то", "куда",
            "между", "многие", "мой", "над", "наиболее", "насколько", "наш", "нет", "никто", "обо", "однако", "она", "они", "оно", "очень",
            "передо", "пока", "после", "поскольку", "потому", "почему", "почти", "при", "про",
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

    # extract set of normalized words for each paper
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


def trend(list_of_values): # just a heuristics
    l = len(list_of_values)
    start_part = list_of_values[0] + list_of_values[1] + list_of_values[2]
    end_part = list_of_values[l-1] + list_of_values[l-2] + list_of_values[l-3]
    if start_part > trend_threshold * end_part:
        return "down"
    elif start_part * trend_threshold < end_part:
        return "up"
    else:
        return "no"

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


# initialize
years_count = dict()  # total for each year
word_count = dict()   # statistics for each normalized word
data = parse_json(path + json_file_name)  # array of pairs [year, set of words]
frequent_word_min = 15

# calculate the number of papers for each word, total and per year
for year in years:
    years_count[str(year)] = 0

for block in data:
    for w in block[1]:
        if w not in word_count:
            word_count[w] = {"all": 0, "2010": 0, "2011": 0, "2012": 0, "2013": 0, "2014": 0, "2015": 0, "2016": 0,
                             "2017": 0}
        word_count[w]["all"] += 1
        word_count[w][block[0]] +=1
        years_count[block[0]] += 1

# get the most frequent words
top_words = dict()
for w in word_count:
    if word_count[w]["all"] >= frequent_word_min:
        top_words[w] = [word_count[w][str(year)] for year in years]

# trend
for w in top_words:
    if trend(top_words[w]) == "up":
        print(w, top_words[w])
