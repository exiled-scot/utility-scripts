import json

class Yasnippet():
    def __init__(self,name,key,command,comment):
        self.name = name
        self.key = key
        self.command = command
        self.comment = comment

snippet_file = "/home/heretek/Programming/awesome-flutter-snippets/snippets/snippets.json"

f = open(snippet_file)
data = json.load(f)
for d in data:
    s_name = d
    s_key = data[d]['prefix']
    s_command = ""
    for i in data[d]['body']:
        s_command = s_command + i + "\n"
    try:
        s_desc = data[d]['description']
    except:
        s_desc = ""
    snippet = """# -*- mode: snippet -*-
# name: %s
# key: %s
# description: %s
# --
%s
"""
    yasnippet = (snippet % (s_name,s_key,s_desc,s_command))
    path = "/home/heretek/Documents/snippets/dart-mode/%s" % s_key
    f = open(path,"a")
    f.write(yasnippet)
    f.close()
f.close()
