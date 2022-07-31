# 21.07.52  Potter's Snap dialogues parser
# Python = 3.9.7

import re
import sys
from os import listdir
from os.path import isfile, join

from rich.pretty import pprint


re_mnt = re.compile("^@(?P<author>[a-zA-Z0-9_]*)(?P<state>:[a-z0-9_])")
re_cmd = re.compile("^:(?P<command>[a-z_]*)(?P<parameters>\(.*\))?[ ]*(?P<string>.*)$")


TOKENS = {
        "NEWLINE": "\n",
        "MENTION": "@",
        "COMMAND": ":",
        "LABEL": "#",
        "COMMENT": "//",
}



class Parser:
    #Current speaker, emotion and branch
    author = "narrator"
    state = "calm"
    mark = "start"
    
    #Pool of strings for current line
    line_pool = []
    
    #Pool of menu and it's options
    menu_pool = {}
    
    #Dict with authors end their states
    characters = {}
    
    def parse_mention(self, mention: str):
        """Parses @a:s string to dict"""
        
        words = mention.split(TOKENS["COMMAND"])
        author = words[0].strip().removeprefix(TOKENS["MENTION"]).removesuffix("\n")
        state = ""
        if author == self.author:
            state = self.state
        if not author:
            if len(words) == 1:
                author = "narrator"
            else:
                author = self.author
        if len(words) > 1:
            state = words[1].rstrip()
        elif not state:
            state = "calm"
        
        if author not in self.characters:
            self.characters[author] = []
            
        if state not in self.characters[author]:
            self.characters[author].append(state)
        return {
            "author": author,
            "state": state,
        }
    
    def parse_command(self, command: str) -> dict:
        """Parses :c(p1; p2) s string to dict"""
        r = {
            "command": "",
            "parameters": [],
            "string": ""
        }
        ext = re_cmd.search(command).groups()
        r["command"] = ext[0]
        if ext[1]:
            for param in ext[1][1:-1].split(';'):
                r["parameters"].append(param)
        r["string"] = ext[2]
        return r
    
    def make_line(self, pool: list) -> dict:
        """Generates line from list"""
        
        text = ""
        for line in pool:
            text += line
        text = text.strip()
        return {
            "type": "line",
            "author": self.author,
            "state": self.state,
            "text": text,
        }
    
    
    def parse(self, path: str) -> dict:
        """Parses file"""
        r = { # Resulting structure
            "characters": {},
            "marks": {
                "start": [],
            }
        }
        
        f = open(path, encoding="utf-8")
        
        for l in f: #Main cycle
            if l.find(TOKENS["COMMENT"]) > -1:
                if l.find("[link=") < 0:  # Дикий костыль. У строк с ссылками не может быть комментов
                    l = l[:l.index(TOKENS["COMMENT"])]
            if l[0] in TOKENS.values():
                if self.line_pool:
                    if self.mark not in r["marks"]:
                        r["marks"][self.mark] = []
                    r["marks"][self.mark].append(self.make_line(self.line_pool))
                    self.line_pool = []
            else:
                self.line_pool.append(l)
                
            
            if l[0] is TOKENS["MENTION"]:
                mention = self.parse_mention(l.split(' ')[0])
                self.author = mention["author"]
                self.state = mention["state"]
              
            elif l[0] is TOKENS["LABEL"]:
                self.state = "calm"
                self.mark = l.removeprefix(TOKENS["LABEL"]).strip()
            if l[0] is TOKENS["COMMAND"]:
                command = self.parse_command(l)
                if command["command"] == "menu":
                    if self.menu_pool:
                        r["marks"][self.mark].append(self.menu_pool)
                        self.menu_pool = {}
                    self.menu_pool["type"] = "menu"
                    self.menu_pool["label"] = command["string"]
                elif command["command"] == "opt":
                    if "opts" not in self.menu_pool:
                        self.menu_pool["opts"] = []
                    option = {}
                    if command["parameters"]:
                        if len(command["parameters"])>0:
                            option["mark"] = command["parameters"][0].removeprefix('#')
                        if len(command["parameters"])>1:
                            mention = self.parse_mention(command["parameters"][1])
                            option["author"] = mention["author"].removeprefix('@')
                            option["state"] = mention["state"]
                        option["text"] = command["string"]
                    self.menu_pool["opts"].append(option)
                else:
                    if self.menu_pool:
                        r["marks"][self.mark].append(self.menu_pool)
                        self.menu_pool = {}
                    if command["command"] == "end":
                        r["marks"][self.mark].append({"type": "end"})
            else:
                if self.menu_pool:
                        r["marks"][self.mark].append(self.menu_pool)
                        self.menu_pool = {}
                    
        r["characters"] = self.characters
        return r




# The next is only needed for console

def choose_file(path="dialogues") -> str:
    """Returns the file path to work with"""
    if len(sys.argv)>1:
        return sys.argv[1]
    else:
        
        dlgs = [f for f in listdir(path) if isfile(join(path, f)) and f[-4:]==".dlg"]
        if dlgs:
            print("Choose .dlg number or paste the path")
            for i, d in enumerate(dlgs):
                print(i, d, sep="\t")
            selected = input('> ')
            if selected.isdecimal():
                if len(dlgs)>int(selected):
                    return join(path, dlgs[int(selected)])
                else:
                    print("No such file")
            elif selected:
                return selected
        else:
            print("Path to the file:")
            if selected := input('> '):
                return selected
            
        return path+"/alice_bob_case.dlg"

def main():
    parser = Parser()
    pprint(parser.parse(choose_file()))


if __name__ == "__main__":
    main()