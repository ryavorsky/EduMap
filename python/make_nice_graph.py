#path = "../data/Direktor_shkoly/"
path = "../data/Nauka_i_shkola/"
json_file_name = "trend_words_and_pairs.json"

import json

f = open(path + json_file_name, "r", encoding="utf-8")
json_lines = f.readlines()

nodes = json.loads(json_lines[0])
edges = json.loads(json_lines[1])

cond_prob = dict()
for pair in edges:
    (w1,w2) = pair.split(" ")
    count1 = float(nodes[w1]["count"])
    count2 = float(nodes[w2]["count"])
    common = float(edges[pair])
    cond_prob[w1 + " " + w2] = common / count1
    cond_prob[w2 + " " + w1] = common / count2
print(cond_prob)

res_file = open(path + "trend_words_and_pairs.tgf", "w", encoding="utf-8")
for node in nodes:
    res_file.write(node + " " + node + "_" + nodes[node]["trend"] + "\n")
res_file.write("#\n")
for pair in cond_prob:
    if  cond_prob[pair] > 0.2:
        res_file.write(pair + "\n")

res_file.close()