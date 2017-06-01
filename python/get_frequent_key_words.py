# First, use mystem.exe -cd --format json titles_and_abstracts.txt titles_and_abstracts.json
import json
import math
import itertools


# Configuration
stopwords_for_all = "../data/stopwords_for_all.txt"
general_words = ["учитель", "ученик", "человек", "работать", "ребенок", "работа", "школа", "образование",
                 "образовательный", "процесс", "новый", "обучение", "вопрос"]
path = "../data/Newtonew/"
input_file_name = "titles_and_abstracts.json"
output_file_name = "frequent_words.txt"
central_words = ["урок", "ученик", "родитель", "знание", "технология"]
N = 560


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


# Auxiliary counting functions
def increment(d, v):
    if v in d:
        d[v] += 1
    else:
        d[v] = 1


def count_frequency(list_of_values):
    res = dict()
    for v in list_of_values:
        increment(res, v)
    return res


# Get data from the json file
def extract_lists_of_words_from_json(words_to_remove=[]):
    stopwords_for_all_file = open(stopwords_for_all, "r", encoding="utf-8")
    stopwords = [w.strip() for w in stopwords_for_all_file.readlines()] + words_to_remove  #  + general_words
    stopwords_for_all_file.close()

    res = []  # will be list of [list of words] for each paper

    f = open(path + input_file_name, "r", encoding="utf-8")
    lines = f.readlines()

    # extract set of normalized words for each paper
    current_line = 0
    while current_line < len(lines):
        title = lines[current_line+1]
        abstract = lines[current_line+2]
        current_line += 4

        title_words = [lemma(e) for e in json.loads(title)]
        abstract_words = [lemma(e) for e in json.loads(abstract)]
        words_list = title_words + abstract_words
        clean_words_list = []
        for w in words_list:
            if (len(w) > 2) and (w not in stopwords):
                clean_words_list.append(w)

        res.append(clean_words_list)

    return res


def tf_idf(list_of_texts):
    all_words = dict()    # for each word the number of documents it appears in
    for text in list_of_texts:
        for w in set(text):
            increment(all_words, w)

    res = []
    for text in list_of_texts:
        tf_idf_values = [[word, tf * math.log2(N/all_words[word])] for word, tf in count_frequency(text).items()]    # frequency of each word in this text
        tf_idf_values.sort(key=lambda x: x[1], reverse=True)
        print(tf_idf_values)
        res.append(tf_idf_values)

    return res    # list of lists of pairs [word, tf_idf]


# The main part
def main():
    papers_data = extract_lists_of_words_from_json([])  # array of [list of words_tf_idf]

    key_words = []
    for words_tf_idf in tf_idf(papers_data):
        half = len(words_tf_idf) // 4   # another heuristics - take the part with bigger tf_idf values
        key_words = key_words + [w[0] for w in words_tf_idf[:half]]
    key_words = [[w, stat] for w,stat in count_frequency(key_words).items()]
    key_words.sort(key=lambda x: x[1], reverse=True)
    key_words = key_words[:500]    # truncate the tail
    print(key_words)

    # Calculate statistics for each pair of key words
    word_pairs = dict()
    set_of_frequent_words = set([e[0] for e in key_words])
    for word_list in papers_data:
        word_set = set_of_frequent_words.intersection(word_list)
        for pair in itertools.combinations(word_set, 2):
            if pair in word_pairs:
                word_pairs[pair] += 1
            else:
                word_pairs[pair] = 1

    # Find nearest
    res_file = open(path + "pairs.tgf", "w", encoding="cp1251")
    for w in set_of_frequent_words:
        res_file.write(w + " " + w + "\n")
    res_file.write("#\n")

    for central_word in set_of_frequent_words:
        nearest = []
        for pair in word_pairs:
            if central_word in pair:
                w = list(set(pair).difference({central_word}))[0]
                #print("урок", pair, word_pairs[pair])
                nearest.append([w, word_pairs[pair]])
                nearest.sort(key=lambda x: x[1], reverse=True)
        K = 2
        delta = 100.0 * (nearest[0][1] - nearest[K-1][1]) / nearest[0][1]
        while (delta < 10.0) and (K < 6):
            K += 1
            delta = 100.0 * (nearest[0][1] - nearest[K-1][1]) / nearest[0][1]

        print(K-1, central_word, str(int(delta)) + "%: ", nearest[0][1], nearest[K-2][1], nearest[:K-1])
        for w in nearest[:K-1]:
            res_file.write(central_word + " " + w[0] + "\n")

    res_file.close()

    print(len(papers_data), " papers analyzed")



main()