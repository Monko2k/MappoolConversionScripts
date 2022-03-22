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
        id = None
        while not id:
            if lengths[ind] == 1:
                mapinput = input(f"Enter link or ID for {cat}: " )
            else:
                mapinput = input(f"Enter link or ID for {cat} {i + 1}: " )
            id = re.search("\d+$", mapinput)
            if id:
                maps.append(id[0])
            else:
                print("Invalid beatmap link/ID")
    if maps:
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
    json.dump(pool, output, indent=2)
    print(f"Wrote to /output/{name}.json")




