import os

os.chdir('../data/Nauka_i_shkola/')
print(os.getcwd())
infile = open("2014-3.txt", 'r', encoding='utf-8')
outfile = open('2014-3new.txt','w', encoding='utf-8')

lines = infile.readlines()
for line in lines:
    if line[0] == "*":
        outfile.write(line[1:].upper())
    else:
        outfile.write(line)

outfile.close()