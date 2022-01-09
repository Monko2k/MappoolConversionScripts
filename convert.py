import re
import json
from statistics import mode
import statistics

def parsePool(name: str):
    with open("./testfiles/" + name + ".tsv") as file:
        lines = file.readlines()
        lines = [line.rstrip().lower().split('\t') for line in lines]
    modregex = "(nm)|(hd)|(hr)|(dt)|(fm)|(tb)|(ez)|(ht)|(fl)"
    idregex = "[\d]{4,}" # matching series of 4 digits or more should work unless the pool is mostly made up of beatmaps w/ id < 4 digits (using 4 because bpm is usually 3 digits)
    modindex = findFreqIndex(lines, modregex)
    idindex = findFreqIndex(lines, idregex)

    if modindex == -1 or idindex == -1: #each beatmap row should have a mod label and id
        print("Couldn't parse pool")
        return
    pool = {
        "name": "test",
        "modgroups": []
    }
    modgroups = {}
    lines = list(filter(lambda x: (len(x) > max(modindex, idindex)), lines))
    lines = [[line[modindex], line[idindex]] for line in lines]
    lines = list(filter(lambda x: (re.search(modregex, x[0]) and re.search(idregex, x[1])), lines))
    for line in lines: print(line)
    for line in lines:
        groupname = re.search("[a-z]+", line[0])[0].upper()
        id = re.search("\d+$", line[1])[0]
        if groupname not in modgroups:
            modgroups[groupname] = []
        modgroups[groupname].append(id)
    
    for item in modgroups:
        pool["modgroups"].append({
            "mod": item,
            "maps": modgroups[item]
        })
    with open("./output/" + name + ".json", "w+") as output: 
        json.dump(pool, output, indent=4)
    





def findFreqIndex(poollines: list, regex: str) -> int:
    indexes = []
    for line in poollines:
        for ind, item in enumerate(line):
            match = re.search(regex, item)
            if match:
                indexes.append(ind)
    if len(indexes) < 5:
        return -1
    return statistics.mode(indexes)


def main():
    parsePool((input("Enter file name: ")))



if __name__ == "__main__":
    main()