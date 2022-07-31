# 22.07.52  Simle console printer
# Python = 3.9.7

import csv
from rich import print


import parser


dialogue = parser.Parser().parse(parser.choose_file())

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

for h in dialogue["marks"]:
    if h != "start":
        print("["+opt_colors[options.index(h)%4]+']-'+h+'>')
    for i in dialogue["marks"][h]:
        
        if i["type"] == "line":
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
            print(i["text"])
        
        elif i["type"] == "menu":
            print(":diamond_with_a_dot:", "[bold blue u]"+i["label"])
            for opt in i["opts"]:
                print("["+opt_colors[len(options)]+"]"+"• "+opt["text"])
                options.append(opt["mark"])
                
        print()
        
