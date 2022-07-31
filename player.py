# 26.07.52  Simle console player
# Python = 3.9.7

import csv
from rich import print


import parser


d = parser.Parser().parse(parser.choose_file())

moods = {
    "calm": "🙂",
    "yawning": "🥱",
    "happy": "😀",
    "sad": "🙁",
    "cool": "😎",
    "smart": "🤓",
    "bored": "😒",
    "scared": "😱",
    "ashamed": "😳",
    }

characters = {}  # Персонажи в формате alias: (name, color)

with open('characters.csv', mode='r', encoding="utf-8") as csv_file:
    # Загружаем персонажей из characters.csv
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count > 0:
            if row:
                characters[row["alias"]] = row["name"], row["color"]
        line_count += 1
    csv_file.close()
    

opt_colors = ["red", "green", "cyan", "yellow"]
options = []



mark = "start"
line = 0

def print_line(i):
    if i["author"] != "narrator":
        print(moods[i["state"]]
              if i["state"] in moods
              else i["state"],
              " [bold "+
              (characters[i["author"]][1]
              if i["author"] in characters
              else "gray")+"]"+
              (characters[i["author"]][0]
              if i["author"] in characters
              else i["author"]))
    
    tags = ""
    tag_pool = ""
    pc = ""
    for c in i["text"]:
        if c == "[" and pc != "\\":
            tag_pool += c
        elif c == "]":
            if tag_pool:
                tag_pool += c
                tags += tag_pool
                tag_pool = ""
            else:
                print(tags+c, end="")
        elif c == "\\":
            if pc == "\\":
                print(tags+c, end="")
        else:
            if tag_pool:
                tag_pool += c
            else:
                print(tags+c, end="")
        pc = c

def print_menu(i):
    opts = []
    print(":diamond_with_a_dot:", "[bold blue u]"+i["label"])
    for opt in i["opts"]:
        print("["+opt_colors[len(options)]+"]"+str(len(opts))+"\t"+opt["text"])
        opts.append(opt["mark"])
        options.append(opt["mark"])
    choice = input("Введи число> ")
    if choice.isdecimal():
        return opts[int(choice)]
    else:
        return opts[0]


while True:
    if line < len(d["marks"][mark]):
        l = d["marks"][mark][line]
        line += 1
        
        if l["type"] == "line":
            print_line(l)
            input()
        elif l["type"] == "menu":
            mark = print_menu(l)
            line = 0
        else:
            break
    else:
        break
