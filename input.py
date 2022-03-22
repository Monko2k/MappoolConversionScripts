import json
import re
import os
modgroups = []
lengths = []
cat_title = ("Nomod", "Hidden", "Hard Rock", "Doubletime", "Freemod", "Tiebreaker")
cats = ("NM", "HD", "HR", "DT", "FM", "TB")
name = input("Enter pool name: ")
for cat in cat_title:
    lengths.append(int(input(f"Enter number of {cat} maps: ")))

for ind, cat in enumerate(cats):
    maps = []
    for i in range(lengths[ind]):
        if lengths[ind] == 1:
            mapinput = input(f"Enter {cat}: " )
        else:
            mapinput = input(f"Enter {cat} {i + 1}: " )

        maps.append(mapinput)
    modgroups.append({
        "mod": cat,
        "maps": maps
    })

pool = {
    "name": name,
    "modgroups": modgroups
}
if not os.path.exists('./output/'):
    os.makedirs('./output/')
with open("./output/" + name + ".json", "w+") as output: 
    json.dump(pool, output, indent=4)




