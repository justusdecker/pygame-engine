import os
'📜'

for root, dirs, files in os.walk("."):
    path = root.split(os.sep)
    con = False
    for d in root.split('\\')[1:]:
        if d.startswith('.') or d.startswith('__'):
            con = True
            break
    if con: continue
    p = os.path.basename(root)
    #if p.startswith('.'): continue
    print((len(path) - 1) * '   ', p)
    for file in files:
        if file.startswith('.') or file.startswith('__'): continue
        print(len(path) * '   ', file)