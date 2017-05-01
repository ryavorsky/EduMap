#path = "../data/Direktor_shkoly/"
#years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
path = "../data/Nauka_i_shkola/"
years = [2013, 2014, 2015, 2016, 2017]
json_file_name = "titles_and_abstracts.json"
frequent_word_min = 12
number_of_trending = 50

import json
import math

excluded = ["автор", "без", "быть", "ваш", "ведь", "весь", "все", "вот", "вряд", "где",
            "данный", "для", "даже", "его", "еще", "если", "зато", "зачастую", "или", "именно",
            "как", "каков", "какой", "когда", "который", "кто", "кто-то", "куда",
            "между", "многие", "мой", "над", "наиболее", "насколько", "наш", "нет", "никто",
            "обо", "однако", "она", "они", "оно", "очень",
            "передо", "пока", "после", "поскольку", "потому", "почему", "почти", "при", "про",
            "раз", "рассматриваться", "сам", "самый", "свой", "себя", "сей", "сейчас", "среди", "статья",
            "так", "также", "такой", "тогда", "только", "тот", "уже", "хотя",
            "чем", "через", "что", "что-то", "чтобы", "это", "этот"]


# order and glue two words
def word_pair(w1, w2):
    if w1 < w2:
        return w1 + " " + w2
    else:
        return w2 + " " + w1


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

    return res


def trend(list_of_values): # just a heuristics
    start_part = list_of_values[0] + list_of_values[1] + list_of_values[2]
    end_part = list_of_values[-1] + list_of_values[-2] + list_of_values[-3]
    return int(100 * math.log2((1 + end_part)/(1 + start_part)) * math.log2(1 + sum(list_of_values)))


# how often two words from the given list appear in a one paper
def count_pairs(words):
    res = dict()
    for d in paper_data:
        list_of_words = list(set(d[1]).intersection(words))
        l = len(list_of_words)
        print(l, list_of_words)
        for i in range(l-1):
            for j in range(i+1,l):
                pair = word_pair(list_of_words[i], list_of_words[j])
                if pair in res:
                    res[pair] = res[pair] + 1
                else:
                    res[pair] = 1
    return res

# initialize
years_count = dict()  # total for each year
word_count = dict()   # statistics for each normalized word
paper_data = parse_json(path + json_file_name)  # array of pairs [year, set of words]

# calculate the number of papers for each word, total and per year
for year in years:
    years_count[str(year)] = 0

for block in paper_data:
    for w in block[1]:
        if w not in word_count:
            word_count[w] = {"all": 0, "2010": 0, "2011": 0, "2012": 0, "2013": 0, "2014": 0, "2015": 0, "2016": 0,
                             "2017": 0}
        word_count[w]["all"] += 1
        word_count[w][block[0]] +=1
        years_count[block[0]] += 1

# get the most trending words
top_words = []
for w in word_count:
    year_by_year = [word_count[w][str(year)] for year in years]
    top_words.append([w, trend(year_by_year), year_by_year])
top_words.sort(key=lambda x: x[1])

top_words_data = top_words[:number_of_trending] + top_words[-number_of_trending:]
top_words_list = [e[0] for e in top_words_data]
print(top_words)

top_words_pairs_count = count_pairs(top_words_list)
top_words_pairs = list(top_words_pairs_count.keys())
top_words_pairs_count = [[k,top_words_pairs_count[k]] for k in top_words_pairs_count]
top_words_pairs_count.sort(key = lambda e: e[1], reverse=True)
print(top_words_pairs_count)

graph_file = open(path + "trend_words.tgf", "w", encoding="windows-1251")

for d in top_words_data:
    if d[1] > 0:
        graph_file.write(d[0] + " " + d[0]+ "-up\n"  )
    else:
        graph_file.write(d[0] + " " + d[0]+ "-down\n"  )
graph_file.write("#\n"  )
for pair in top_words_pairs_count:
    graph_file.write(pair[0].replace("_", " ") + "\n")

graph_file.close()

