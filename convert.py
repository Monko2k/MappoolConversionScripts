import re
import json
from statistics import mode
import statistics
from typing import Protocol

def parsePool(name: str):
    with open("./testfiles/" + name + ".tsv") as file:
        lines = file.readlines()
        lines = [line.rstrip().lower().split('\t') for line in lines]
    modregex = "(nm)|(hd)|(hr)|(dt)|(fm)|(tb)|(ez)|(fl)" # halftime not included for now
    idregex = "[\d]{4,}$" # match 4+ digits as beatmap id, can't differentiate <4 from BPM 

    modindex = findFreqIndex(lines, modregex)
    idindex = findFreqIndex(lines, idregex)

    if idindex == -1: #each beatmap row should have a mod label and id
        print("Couldn't parse pool")
        return
    
    if modindex != -1:
        # see if the modindex makes sense 
        if findCountIndex(lines, idregex, idindex) != findCountIndex(lines, modregex, modindex):
            modindex = -1

    pool = {
        "name": "test",
        "modgroups": []
    }
    modgroups = {}
    if modindex != -1: 
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
    else: # case for mod group labels instead of individual ones (awesome) 
        clearedlines = []
        for line in lines:
            mod = checkForLabel(line)
            if mod != "": clearedlines.append(mod)
            if len(line) > idindex:
                match = re.search(idregex, line[idindex])
                if match:
                    clearedlines.append(match[0])
                else: # search for mod labels in the case where the first row of the group has an extra element
                    if mod != "":
                        match = re.search(idregex, line[idindex + 1])
                        if match:
                            clearedlines.append(match[0])
        if re.search(idregex, clearedlines[0]): # first line should be a mod label
            print("Failed to parse")
            return
        label = clearedlines[0]
        for line in clearedlines:
            if re.search(idregex, line):
                modgroups[label].append(line)
            else:
                label = line
                modgroups[label] = []
    for item in modgroups:

        pool["modgroups"].append({
            "mod": item,
            "maps": modgroups[item]
        })
    with open("./output/" + name + ".json", "w+") as output: 
        json.dump(pool, output, indent=4)
    
def findCountIndex(poollines: list, regex: str, index: int) -> int:
    count = 0
    for line in poollines:
        if len(line) > index and re.search(regex, line[index]): count += 1
    return count

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

def checkForLabel(line: list) -> str:
    # this is awesome
    for item in line:
        if re.search("(no[-\s]?mod)|(^nm$)", item): return "NM"
        if re.search("(hidden)|(^hd$)", item): return "HD"
        if re.search("(hard[-\s]?rock)|(^hr$)", item): return "HR"
        if re.search("(double[-\s]?time)|(^dt$)", item): return "DT"
        if re.search("(free[-\s]?mod)|(^fm$)", item): return "FM"
        if re.search("(tie[-\s]?breaker)|(^tb$)", item): return "TB"
        if re.search("(easy)|(^ez$)", item): return "EZ"
        if re.search("(flash[-\s]?light)|(^fl$)", item): return "FL"
    return ""


def main():
    parsePool(input("Enter file name: "))



if __name__ == "__main__":
    main()