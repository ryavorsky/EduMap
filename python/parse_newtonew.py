import os
import sys
from bs4 import BeautifulSoup

stop_words = ["У вас есть интересная новость", "Расскажите нам!", "Вход через соц.сети", "2014-2017 Newtonew",
              "Просветительский медиа-проект об образовании", "с разрешения редакции Newtonew"]
os.chdir('../data/Newtonew/download/')
f_titles_and_abstracts = open("../titles_and_abstracts.txt", "w", encoding="utf-8")


def div_author_class(css_class):
    return (css_class == "io-author") or (css_class == "t013__autor-title")

file_names = os.listdir()
print(os.getcwd(), os.listdir())

res_data = []

for file_name in file_names:

    f_in = open(file_name, "r", encoding="utf-8")
    source_text = f_in.read()
    f_in.close()

    soup = BeautifulSoup(source_text, 'html.parser')

    print("\n#####" + file_name)

    text = ''

    for node in soup.find_all("p"):
        if not node.has_attr('class') and not node.has_attr('style'):
            for s in node.strings:
                if not any(stop_word in str(s) for stop_word in stop_words):
                    text += " " + str(s)
    print(text)

    date = list(soup.find("p", attrs = {"class": "io-article-footer"}))[0].strip()
    year = date.split(" ")[2].split(",")[0]
    author = soup.find("div", class_=div_author_class).text
    title = soup.find("h1").text
    print(year, author, title)

    f_titles_and_abstracts.write(year + "\t" + file_name.split(".")[0] + "\n" + title.upper() + "\n" + text.strip() + "\n\n")

f_titles_and_abstracts.close()

