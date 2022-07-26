# 26.07.52  .dlg to .json converter
# Python = 3.9.7

import json
import sys

from rich import print


import parser


file_path = parser.choose_file()
dialogue = parser.Parser().parse(file_path)

if len(sys.argv) > 2:
    result_path = sys.argv[2]
else:
    result_path = file_path[:-4] + ".json"


with open(result_path, 'w') as json_file:
    json.dump(dialogue, json_file, ensure_ascii=False)
    print("File has been saved as", result_path)
