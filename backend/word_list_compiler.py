import os
import sys
import csv
import pandas as pd

frequencies = open(os.path.join(sys.path[0], "word_frequencies.csv"), "r",encoding="utf-8")
godan = open(os.path.join(sys.path[0], "godan_verbs_list.csv"), "r",encoding="utf-8")
ichidan = open(os.path.join(sys.path[0],"ichidan_verbs_list.csv"),"r",encoding="utf-8")

# a = pd.read_csv(os.path.join(sys.path[0], "ichidan_verbs_list.csv"))
# b = pd.read_csv(os.path.join(sys.path[0], "word_frequencies.csv"))

# merged = a.merge(b,left_on="Verb",right_on="Expression")

total = 0

godan_list = []
ichidan_list = []
freq_list = []
irregular_list = [
    {"Verb":"する","Hiragana":"する","Meaning":"to do","Transitivity":"t","type":"suru"},
    {"Verb":"来る","Hiragana":"くる","Meaning":"to come","Transitivity":"i","type":"kuru"}
]


for item in csv.DictReader(godan):
    item["type"] = "godan"
    godan_list.append(item)

for item in csv.DictReader(ichidan):
    item["type"] = "ichidan"
    ichidan_list.append(item)    

frequency_dict = csv.DictReader(frequencies)

for item in csv.DictReader(frequencies):
    freq_list.append(item)


for word in godan_list+ichidan_list+irregular_list:
    for item in freq_list:
        if word["Verb"] == item["Expression"]:
            word["freq"] = int(item["Occurences"])
            total += int(item["Occurences"])
            #print(word["Verb"])

print("aaa")

for word in godan_list+ichidan_list+irregular_list:
    #print(word)
    word["relfreq"] = word["freq"] / total * 1000
    word["proficiency"] = 0
    word["prio"] = (1-word["proficiency"]) * (1 + (word["relfreq"] / 1000))
    word["kanji"] = word.pop("Verb")
    word["hiragana"] = word.pop("Hiragana")
    word["transitivity"] = word.pop("Transitivity")
    word["english"] = word.pop("Meaning")
#godan_list[0]["proficiency"] += 0.25

# godan_list.pop(221)

max = 0
max_index = 0
for i in range(len(godan_list+ichidan_list+irregular_list)):
    if (godan_list+ichidan_list+irregular_list)[i]["prio"] > max:
        max = (godan_list+ichidan_list+irregular_list)[i]["prio"]
        max_index = i


for item in frequency_dict:
    total += int(item["Occurences"])


#print(godan_list[0])

output = open(os.path.join(sys.path[0], "words.csv"), "w",encoding="utf-8")
fieldnames = ["kanji","hiragana","transitivity","english","type","freq","relfreq","proficiency","prio"]
writer = csv.DictWriter(output, fieldnames=fieldnames)
writer.writeheader()
writer.writerows(godan_list+ichidan_list+irregular_list)
output.close()


frequencies.close()
godan.close()
ichidan.close()

file = open(os.path.join(sys.path[0], "words.csv"), "r",encoding="utf-8")

words = csv.DictReader(file)

word_list = []

for item in words:
    word_list.append(item)

print(word_list)

file.close()