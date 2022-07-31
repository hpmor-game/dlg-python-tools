# 31.07.52  .dlg to .ron converter
# Python = 3.10.5


import sys

import pyron

import parser


file_path = parser.choose_file()
dialogue = parser.Parser().parse(file_path)

if len(sys.argv) > 2:
    result_path = sys.argv[2]
else:
    result_path = file_path[:-4] + ".ron"


with open(result_path, 'w') as ron_file:
    ron_file.write(pyron.to_string(dialogue))
    print("File has been saved as", result_path)
