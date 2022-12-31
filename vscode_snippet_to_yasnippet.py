import json

import sys

snippet_file = sys.argv[1]
dir_path = sys.argv[2]

class Yasnippet():
    def __init__(self,name,key,command,comment):
        self.name = name
        self.key = key
        self.command = command
        self.comment = comment

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
    path = "%s/%s" % (dir_path,s_key)
    f = open(path,"a")
    f.write(yasnippet)
    f.close()
f.close()

print("Done!")
