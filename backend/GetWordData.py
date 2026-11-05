import random
import os
import sys
import json
import math
import time
import csv

#code from https://github.com/aleckretch/Romaji-to-Japanese-Converter/blob/master/convert.py
#romanization has received slight changes
import convert 

def importStats(user):
    statsjson = open(os.path.join(sys.path[0], "users/"+user+"/stats.json"), "r",encoding="utf-8")
    stats = json.loads(statsjson.read())
    return stats

def saveStats(stats,user):
    statsjson = open(os.path.join(sys.path[0], "users/"+user+"/stats.json"), "w",encoding="utf-8")
    statsjson.write(json.dumps(stats))

def choose_conjugation(word,options): #picks random conjugations

    choices = {}

    chosen_options = dict(random.sample(list(options.items()),random.randint(1,len(options))))

    for option in options:
        if option in chosen_options:
            choices[option] = options[option][1]
        else:
            choices[option] = options[option][0]

    try:
        if choices["tense"] == "past":
            if random.randint(0,1) == 0:
                choices["politeness"] = "casual"
            if random.randint(0,1) == 0:
                choices["negative"] = "affirmative"
    except:
        pass

    try:
        if choices["aspect"] == "stative":
            if word["hiragana"] in ["いる","いる","ある"]:
                choices["aspect"] = "base"
                choices["tense"] = "aspect"
    except:
        pass
        

    return choices
        
def choose_word(full_list,stats,config): #don't be stupid
    # word = full_list[random.randint(0,len(full_list)-1)]

    max = 0
    max_index = 0
    for i in range(len(full_list)):
        full_list[i]["prio"] = (1-float(full_list[i]["proficiency"])) * ((float(full_list[i]["relfreq"])))

        config_check = True

        if config["godan"] == 0 and (full_list[i]["type"] == "godan"):
            config_check = False
        elif config["godan"] == "level" and (full_list[i]["type"] == "godan"):
            if stats["level"] < 10:
                config_check = False

        if config["irregular"] == 0 and (full_list[i]["type"] == "suru" or full_list[i]["type"] == "kuru"):
            config_check = False
        elif config["irregular"] == "level" and (full_list[i]["type"] == "suru" or full_list[i]["type"] == "kuru"):
            if stats["level"] < 45:
                config_check = False


        if (float((full_list)[i]["prio"]) > max) and (config_check == True):
            max = float((full_list)[i]["prio"])
            max_index = i

    return full_list[max_index]

def conjugateSuru(choices,prev=""): #special conjugation tab for suru
    if choices["aspect"] == "stative":
        correct_form = "し"
        steps.append(prev+correct_form)
        correct_form += "て"
        steps.append(prev+correct_form)
        aux_choices = choices.copy()
        aux_choices["aspect"] = "base"
        correct_form += getCorrectForm({"kanji":"いる","hiragana":"いる","english":"aux","type":"ichidan"},aux_choices,prev+correct_form)
    else:
        if choices["politeness"] == "polite":
            correct_form = "し"
            steps.append(prev+correct_form)
            correct_form += getMasuEnding(choices,prev+correct_form)
        else:
            if choices["polarity"] == "negative":
                correct_form = "し"
                steps.append(prev+correct_form)
                aux_choices = choices.copy()
                aux_choices["polarity"] = "affirmative"
                correct_form += getCorrectForm({"kanji":"ない","hiragana":"ない","english":"aux","type":"i"},aux_choices,prev+correct_form)
            else:
                if choices["tense"] == "past":
                    correct_form = "し"
                    steps.append(prev+correct_form)
                    correct_form += "た"
                    steps.append(prev+correct_form)
                else:
                    correct_form = "する"
    return correct_form

def conjugateKuru(choices,prev=""): #special conjugation tab for kuru
    if choices["aspect"] == "stative":
        correct_form = "き"
        steps.append(prev + correct_form)
        correct_form += "て"
        steps.append(prev + correct_form)
        aux_choices = choices.copy()
        aux_choices["aspect"] = ""
        correct_form += getCorrectForm({"kanji":"いる","hiragana":"いる","english":"aux","type":"ichidan"},aux_choices,prev+correct_form)
    else:
        if choices["politeness"] == "polite":
            correct_form = "き"
            steps.append(prev + correct_form)
            correct_form += getMasuEnding(choices,prev+correct_form)
        else:
            if choices["polarity"] == "negative":
                correct_form = "こ"
                steps.append(prev + correct_form)
                aux_choices = choices.copy()
                aux_choices["polarity"] = "affirmative"
                correct_form += getCorrectForm({"kanji":"ない","hiragana":"ない","english":"aux","type":"i"},aux_choices,prev+correct_form)
            else:
                if choices["tense"] == "past":
                    correct_form = "き"
                    steps.append(prev + correct_form)
                    correct_form += "た"
                    steps.append(prev + correct_form)
                else:
                    correct_form = "くる"
    return correct_form

def getCorrectForm(word,choices,prev=""): #produces the correct verb form
    global irregular
    global irregular_type
    
    aux_choices = {}

    polite_verbs = [
        "いらっしゃる",
        "おっしゃる",
        "くださる",
        "ござる",
        "なさる"
    ]

    euphony_irregulars = [
        "とう",
        "こう"
    ]
    
    table = {
        "う":{"u":"う","i":"い","a":"わ","euphonic_a":"った","euphonic_e":"って"},
        "つ":{"u":"つ","i":"ち","a":"た","euphonic_a":"った","euphonic_e":"って"},
        "る":{"u":"る","i":"り","a":"ら","euphonic_a":"った","euphonic_e":"って"},
        "む":{"u":"む","i":"み","a":"ま","euphonic_a":"んだ","euphonic_e":"んで"},
        "ぬ":{"u":"ぬ","i":"に","a":"な","euphonic_a":"んだ","euphonic_e":"んで"},
        "ぶ":{"u":"ぶ","i":"び","a":"ば","euphonic_a":"んだ","euphonic_e":"んで"},
        "く":{"u":"く","i":"き","a":"か","euphonic_a":"いた","euphonic_e":"いて"},
        "ぐ":{"u":"ぐ","i":"ぎ","a":"が","euphonic_a":"いだ","euphonic_e":"いで"},
        "す":{"u":"す","i":"し","a":"さ","euphonic_a":"した","euphonic_e":"して"},
        "い":{"u":"い","i":"い","a":"い","euphonic_a":"い","euphonic_e":"い"}
    }

    if word["type"] == "desu":
        if choices["politeness"] == "polite":
            correct_form = "です"
            steps.append(prev+correct_form)
            if choices["tense"] == "past":
                correct_form = correct_form[0:-1] + "した"
                steps.append(prev+correct_form)
        else:
            correct_form = "だ"
            steps.append(prev+correct_form)
            if choices["tense"] == "past":
                correct_form += "った"
                steps.append(prev+correct_form)
    
    elif word["type"] == "i": 
        steps.append(prev + word["hiragana"])
        correct_form = word["hiragana"][0:-1]
        if word["hiragana"] == "いい" and choices != {
            "politeness":"casual",
            "polarity":"affirmative",
            "tense":"nonpast",
            "aspect":"base"
        }:
            irregular = True
            irregular_type = "いい is conjugated as if it were よい"
            correct_form = "よ"
        if choices["polarity"] == "negative":
            correct_form += "く"
            aux_choices = choices.copy()
            steps.append(prev+correct_form)
            aux_choices["polarity"] = "affirmative"
            correct_form += getCorrectForm({"kanji":"ない","hiragana":"ない","english":"aux","type":"i"},aux_choices,prev+correct_form)
        else:
            if choices["tense"] == "past":
                correct_form += "かった"

                steps.append(prev + correct_form)

                if choices["politeness"] == "polite":
                    aux_choices = choices.copy()
                    aux_choices["tense"] = "nonpast"
                    correct_form += getCorrectForm({"kanji":"です","hiragana":"です","english":"aux","type":"desu"},aux_choices)
            else:
                correct_form += "い"
                if choices["politeness"] == "polite":
                    correct_form += getCorrectForm({"kanji":"です","hiragana":"です","english":"aux","type":"desu"},choices)

    elif word["type"] == "suru":
        irregular = True
        irregular_type = "する is fully irregular"
        steps.append(prev + word["hiragana"])
        #correct_form = "する"
        correct_form = conjugateSuru(choices)

    elif word["type"] == "kuru":
        irregular = True     
        irregular_type = "くる is fully irregular"
        steps.append(prev + word["hiragana"])
        #correct_form = "くる"
        correct_form = conjugateKuru(choices)

    elif word["type"] == "ichidan":

        steps.append(prev + word["hiragana"])

        correct_form = word["hiragana"][0:-1]

        if choices["aspect"] == "stative":
            aux_choices = choices.copy()
            aux_choices["aspect"] = ""
            correct_form += "て"
            steps.append(prev+correct_form)
            correct_form += getCorrectForm({"kanji":"いる","hiragana":"いる","english":"aux","type":"ichidan"},aux_choices,prev+correct_form)

            #steps.append(correct_form)
        
        else:
            if choices["politeness"] == "polite":
                correct_form += getMasuEnding(choices,prev+prev+correct_form)
            else:
                if choices["polarity"] == "negative":
                    aux_choices = choices.copy()
                    aux_choices["polarity"] = "affirmative"
                    correct_form += getCorrectForm({"kanji":"ない","hiragana":"ない","english":"aux","type":"i"},aux_choices,prev+correct_form)

                else:
                    if choices["tense"] == "past":
                        
                        correct_form += "た"
                        steps.append(correct_form)
                    else:
                        correct_form += "る"

    elif word["type"] =="godan":

        steps.append(prev + word["hiragana"])

        correct_form = word["hiragana"][0:-1]
        stems = table[word["hiragana"][-1]]

        if choices["aspect"] == "stative":
            if word["kanji"][-2:] == "行く":
                correct_form += "って"
                irregular = True
                irregular_type = "The past of いく is いった"
                steps.append(prev + correct_form)
                aux_choices = choices.copy()
                aux_choices["stative"] = "base"
                correct_form += getCorrectForm({"kanji":"いる","hiragana":"いる","english":"aux","type":"ichidan"},aux_choices,prev+correct_form)
                
            elif word["hiragana"] in euphony_irregulars:
                correct_form += "て",
                irregular = True
                irregular_type = "A few verbs ending in oう have a past tense of oうた"
                steps.append(prev + correct_form)
                aux_choices = choices.copy()
                aux_choices["stative"] = "base"
                correct_form += getCorrectForm({"kanji":"いる","hiragana":"いる","english":"aux","type":"ichidan"},aux_choices,prev+correct_form)     
            else:
                correct_form += stems["euphonic_e"]

                steps.append(prev + correct_form)
                
                aux_choices["politeness"] = choices["politeness"]
                aux_choices["polarity"] = choices["polarity"]
                aux_choices["tense"] = choices["tense"]
                aux_choices["aspect"] = "base"

                correct_form += getCorrectForm({"kanji":"いる","hiragana":"いる","english":"aux","type":"ichidan"},aux_choices,prev+correct_form)
        else:
            if choices["politeness"] == "polite":
                if word["hiragana"] in polite_verbs:
                    correct_form += "い"
                    correct_form += getMasuEnding(choices,prev+prev+correct_form)
                    irregular = True
                    irregular_type = "A small set of polite verbs drop the /r/ in ます constructions"
                else:
                    correct_form += stems["i"]
                    correct_form += getMasuEnding(choices,prev+correct_form)
            else:
                if choices["polarity"] == "negative":
                    correct_form += stems["a"]
                    if word["hiragana"] == "ある":
                        correct_form = ""
                        irregular = True     
                        irregular_type = "ある negative is ない"
                    aux_choices = choices.copy()
                    aux_choices["polarity"] = "affirmative"               
                    correct_form += getCorrectForm({"kanji":"ない","hiragana":"ない","english":"aux","type":"i"},aux_choices,prev+correct_form)
                else:
                    if choices["tense"] == "past":
                        if word["kanji"][-2:] == "行く":
                            correct_form += "った"
                            irregular = True
                            irregular_type = "The past of いく is いった"
                        elif word["hiragana"] in euphony_irregulars:
                            correct_form += "た",
                            irregular = True
                            irregular_type = "A few verbs ending in oう have a past tense of oうた"
                        else:
                            correct_form += stems["euphonic_a"]
                            steps.append(prev + correct_form)
                    else:
                        correct_form += stems["u"]

    #print(correct_form)



    return correct_form #,correct_form_kanji

def getMasuEnding(choices,prev=""): #produces the correct verb form continuing from masu
    masu_ending = "ます"
    steps.append(prev+masu_ending)

    if choices["polarity"] == "affirmative":
        if choices["tense"] == "past":
            masu_ending = masu_ending[0:-1] + "した"
            steps.append(prev+masu_ending)

    elif choices["polarity"] == "negative":
        masu_ending = masu_ending[0:-1] + "せん"
        steps.append(prev+masu_ending)
        if choices["tense"] == "past":
            masu_ending += getCorrectForm({"kanji":"です","hiragana":"です","english":"aux","type":"desu"},choices,prev+masu_ending)
            

    return masu_ending

def getNaiEnding(choices): #produces the correct verb form continuing from nai
    if choices["tense"] == "nonpast":
        nai_ending = "ない"
    if choices["tense"] == "past":
        nai_ending = "なかった"

    return nai_ending

def importConfig(user): #imports the config file
    global config
    config_file = open(os.path.join(sys.path[0], "users/"+user+"/config.json"),"r",encoding="utf-8")
    config = json.loads(config_file.read())

def getChoiceMul(word,choices): #calculates the xp multiplier
    if choices["polarity"] == "negative":
        neg_mul = 1.1
    else:
        neg_mul = 1
    if choices["tense"] == "past":
        past_mul = 1.15
    else:
        past_mul = 1
    if word["type"] == "godan":
        type_mul = 1.1
    elif irregular == True:
        type_mul = 5
    else:
        type_mul = 1

    return neg_mul * type_mul * past_mul

def applyOptionsConfig(options,config,stats):
    if config["stative"] == 0:
        options.pop("aspect")
    elif config["stative"] == "level":
        if stats["level"] < 15:
            options.pop("aspect")

    if config["past"] == 0:
        options.pop("tense")
    elif config["past"] == "level":
        if stats["level"] < 8:
            options.pop("tense")

    if config["polite"] == 0:
        options.pop("politeness")
    elif config["polite"] == "level":
        if stats["level"] < 5:
            options.pop("politeness")
    return options

def createWordList(user):
    file = open(os.path.join(sys.path[0], "users/"+user+"/words.csv"), "r",encoding="utf-8")

    words = csv.DictReader(file)

    global word_list
    word_list = []

    for item in words:
        word_list.append(item)

    file.close()

    return word_list

def createPrintOutput(config,choices):
    printoutput = ""
    if config["showtype"] == True:
        printoutput += word["type"]+" "
    if choices["politeness"] == "polite":        
        printoutput += choices["politeness"]+" "
    if choices["polarity"] == "negative":
        printoutput += choices["polarity"]+" "
    if choices["tense"] == "past":
        printoutput += choices["tense"]+" "
    if choices["aspect"] == "stative":
        printoutput += choices["aspect"]+" "
    if printoutput == "":
        printoutput = "base "
    return printoutput

def saveWords(word_list,user):
    output = open(os.path.join(sys.path[0], "users/"+user+"/words.csv"), "w",encoding="utf-8")
    fieldnames = ["kanji","hiragana","transitivity","english","type","freq","relfreq","proficiency","prio"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(word_list)
    output.close()

def getUsers():
    user_list = open(os.path.join(sys.path[0], "users.json"), "r",encoding="utf-8")
    return user_list.read()

def createUser(user="fallback"):

    user = "_".join(user.split())

    users = open(os.path.join(sys.path[0], "users.json"), "r",encoding="utf-8")
    user_list = json.loads(users.read())
    users.close()
    try:
        os.mkdir(os.path.join(sys.path[0], "users/"+user))
        user_list["users"].append(user)
        users = open(os.path.join(sys.path[0], "users.json"), "w",encoding="utf-8")
        users.write(json.dumps(user_list))
        users.close()
    except:
        pass


    config_base = open(os.path.join(sys.path[0], "users/default/config.json"), "r",encoding="utf-8")
    config_new = open(os.path.join(sys.path[0], "users/"+user+"/config.json"), "w",encoding="utf-8")
    config_new.write(config_base.read())
    config_base.close()
    config_new.close()

    stats_base = open(os.path.join(sys.path[0], "users/default/stats.json"), "r",encoding="utf-8")
    stats_new = open(os.path.join(sys.path[0], "users/"+user+"/stats.json"), "w",encoding="utf-8")
    stats_new.write(stats_base.read())
    stats_base.close()
    stats_new.close()

    words_base = open(os.path.join(sys.path[0], "users/default/words.csv"), "r",encoding="utf-8")
    words_new = open(os.path.join(sys.path[0], "users/"+user+"/words.csv"), "w",encoding="utf-8")
    words_new.write(words_base.read())
    words_base.close()
    words_new.close()


def getJson(user="fallback"):
    global word
    global choices

    stats = importStats(user)
    importConfig(user)

    options = {
        "politeness":["casual","polite"],
        "polarity":["affirmative","negative"],
        "tense":["nonpast","past"],
        "aspect":["base","stative"]
    }

    options_stative = options.copy()

    options = applyOptionsConfig(options,config,stats)

    word_list = createWordList(user)

    word = choose_word(word_list,stats,config)
    choices = choose_conjugation(word,options)

    for option in options_stative:
        if not option in choices:
            choices[option] = options_stative[option][0]

    print(chr(sum(range(ord(min(str(not())))))))

    jsonoutput = {}
    global current_streak
    global irregular
    global irregular_type
    irregular = False
    irregular_type = "none"

    # prints options in case relevant
    printoutput = createPrintOutput(config,choices)
    jsonoutput["options"] = printoutput[:-1]

    # prints the word in japanese and english
    jsonoutput["hiragana"] = word["hiragana"]
    jsonoutput["english"] = word["english"].strip()

    special_rewards = ["マンボ","ウェイ","走れ走れうまむすめ","ばくしんばくしんばくしん","張り切っていこう","早え～"]


    if stats["current_streak"] % 5 == 0 and stats["current_streak"] != 0:
        current_streak_output = str(stats["current_streak"]) + " " + special_rewards[random.randint(0,len(special_rewards)-1)]
        jsonoutput["current_streak"] = "Current Streak: " + str(current_streak_output)
    else:
        jsonoutput["current_streak"] = "Current Streak: " + str(stats["current_streak"])

    global start_time
    start_time = time.time()
    jsonoutput["level"] = "Level: " + str(int(stats["level"]))

    #jsonoutput["progress"] = str(round(stats["progress"] * 100,2)) + "%"
    jsonoutput["progress"] = int(round(stats["progress"] * 100,2)) #swap for raw number
    return json.dumps(jsonoutput)

def gradeAnswer(answer,user="fallback"):

    stats = importStats(user)

    global steps
    steps = []

    global current_streak
    global irregular
    global irregular_type

    jsonoutput = {}
    
    answer = convert.romajiToJapanese(answer)

    # word = {"kanji":"縮める","hiragana":"ちぢめる","english":"aux","type":"ichidan"}
    # choices = {
    #         "politeness":"casual",
    #         "polarity":"affirmative",
    #         "tense":"nonpast",
    #         "aspect":"base"
    #     }

    for i in range(len(word["kanji"])):
        for j in range(len(word["hiragana"])):
            if word["kanji"][:i]+word["hiragana"][j:] == word["kanji"]:
                kanji_adjusts = [i,j]
                break


    # computes the correct answer
    correct_form = getCorrectForm(word,choices)
    #print(correct_form,word["kanji"])

    debug = open(os.path.join(sys.path[0], "debug.txt"), "a",encoding="utf-8")

    if (correct_form == answer) or (word["kanji"][:kanji_adjusts[0]] + correct_form[kanji_adjusts[1]:] == answer):

        debug.write(correct_form+""+answer+" correct\n")

        word["proficiency"] = (float(word["proficiency"]) + 1) / 2

        stats["current_streak"] += 1

        jsonoutput["result"] = "correct"

        xp_mul = getChoiceMul(word,choices)

        stats["response_time"] = min(time.time() - start_time,30)
        jsonoutput["response_time"] = str(round(time.time() - start_time,1)) + "s"

        stats["xp"] += (1 + math.log(stats["current_streak"]+1,4)) * xp_mul * (1 + ((30 - stats["response_time"]) / 100))
        stats["level"] = math.sqrt(stats["xp"]+9) - 3
        stats["progress"] = (stats["xp"] - (math.floor(stats["level"]) ** 2 + 6 * math.floor(stats["level"]))) / ((math.ceil(stats["level"]) ** 2 + 6 * math.ceil(stats["level"])) - (math.floor(stats["level"]) ** 2 + 6 * math.floor(stats["level"])))

    else:

        debug.write(correct_form+""+answer+" incorrect\n")
        
        word["proficiency"] = (float(word["proficiency"]) - 0) / 2

        stats["current_streak"] = 0
        if answer != "":
            jsonoutput["result"] = "incorrect"
        else:
            jsonoutput["result"] = "didn't submit an answer"

        try:
            jsonoutput["step0"] = steps[0]
        except:
            pass
        try:
            jsonoutput["step1"] = steps[1]
        except:
            pass
        try:
            jsonoutput["step2"] = steps[2]
        except:
            pass
        try:
            jsonoutput["step3"] = steps[3]
        except:
            pass
        try:
            jsonoutput["step4"] = steps[4]
        except:
            pass
        try:
            jsonoutput["step5"] = steps[5]
        except:
            pass
        try:
            jsonoutput["step6"] = steps[6]
        except:
            pass
        try:
            jsonoutput["step7"] = steps[7]
        except:
            pass

        if answer in steps[1:]:
            jsonoutput["misconjugation"] = "You forgot part of the conjugation"
        
        word_godan = word.copy()
        word_godan["type"] = "godan"
        word_ichidan = word.copy()
        word_ichidan["type"] = "ichidan"

        #Checks whether the mistake was using the word verb type
        godan_form = getCorrectForm(word_godan,choices)
        ichidan_form = getCorrectForm(word_ichidan,choices)

        if answer == godan_form:
            jsonoutput["misconjugation"] = "You conjugated the word as if it were a godan word"

        elif answer == ichidan_form:
            jsonoutput["misconjugation"] = "You conjugated the word as if it were a ichidan word"

        if irregular == True:
            jsonoutput["irregularity"] = "Irregular:", irregular_type

        
        jsonoutput["correct_form"] = correct_form
        #print(correct_form)
    
    saveStats(stats,user)
    saveWords(word_list,user)
    debug.close()
    return json.dumps(jsonoutput)

# count = 0
# while True:
#    count += 1
#    print(count)
#    getJson()
#    gradeAnswer("")
   #time.sleep(0)
# getJson()
# gradeAnswer(input())

# print(steps)