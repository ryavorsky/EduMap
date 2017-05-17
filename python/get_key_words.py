# First, use mystem.exe -cd --format json titles_and_abstracts.txt titles_and_abstracts.json
import json
import math

# Configuration
stopwords_for_all = "../data/stopwords_for_all.txt"
path = "../data/Newtonew/"
json_file_name = "titles_and_abstracts.json"

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
def extract_lists_of_words_from_json(words_to_remove):
    res = [] # will be list of [list of words] for each paper

    f = open(path + json_file_name, "r", encoding="utf-8")
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
            if (len(w) > 2) and (w not in words_to_remove):
                clean_words_list.append(w)

        res.append(clean_words_list)

    return res


# The main part
def main():
    stopwords_for_all_file = open(stopwords_for_all, "r", encoding="utf-8")
    stopwords = [w.strip() for w in stopwords_for_all_file.readlines()]
    print(stopwords)

    word_count = dict()   # statistics for each normalized word
    papers_data = extract_lists_of_words_from_json(stopwords)  # array of [list of words]

    # calculate the number of papers for each word
    for word_list in papers_data:
        for w in word_list:
            if w not in word_count:
                word_count[w] = 0
            word_count[w] += 1

    # get the most important words
    top_words = []
    for w in word_count:
        top_words.append([w, word_count[w]])

    top_words.sort(key=lambda x: x[1], reverse=True)

    print(top_words[-1000:])

    res_file = open(path+"frequent_words.txt", "w", encoding="utf-8")
    for data in top_words[:1000]:
        res_file.write(data[0] + "\t" + str(data[1]) + "\n")
    res_file.close()

main()