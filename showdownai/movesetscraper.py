from selenium import webdriver
import time
import json
from gamestateEdited import Pokemon
import re

def convertNature(nature):
    nature_dict = {"hp": 1.0, "patk": 1.0, "pdef": 1.0, "spatk": 1.0, "spdef": 1.0, "spe": 1.0}
    if nature == "Lonely":
        nature_dict['patk'] = 1.1
        nature_dict['pdef'] = 0.9
    elif nature == "Brave":
        nature_dict['patk'] = 1.1
        nature_dict['spe'] = 0.9
    elif nature == "Adamant":
        nature_dict['patk'] = 1.1
        nature_dict['spatk'] = 0.9
    elif nature == "Naughty":
        nature_dict['patk'] = 1.1
        nature_dict['spdef'] = 0.9
    elif nature == "Bold":
        nature_dict['pdef'] = 1.1
        nature_dict['patk'] = 0.9
    elif nature == "Relaxed":
        nature_dict['pdef'] = 1.1
        nature_dict['spe'] = 0.9
    elif nature == "Impish":
        nature_dict['pdef'] = 1.1
        nature_dict['spatk'] = 0.9
    elif nature == "Lax":
        nature_dict['pdef'] = 1.1
        nature_dict['spdef'] = 0.9
    elif nature == "Timid":
        nature_dict['spe'] = 1.1
        nature_dict['patk'] = 0.9
    elif nature == "Hasty":
        nature_dict['spe'] = 1.1
        nature_dict['pdef'] = 0.9
    elif nature == "Jolly":
        nature_dict['spe'] = 1.1
        nature_dict['spatk'] = 0.9
    elif nature == "Naive":
        nature_dict['spe'] = 1.1
        nature_dict['spdef'] = 0.9
    elif nature == "Modest":
        nature_dict['spatk'] = 1.1
        nature_dict['patk'] = 0.9
    elif nature == "Mild":
        nature_dict['spatk'] = 1.1
        nature_dict['pdef'] = 0.9
    elif nature == "Quiet":
        nature_dict['spatk'] = 1.1
        nature_dict['spe'] = 0.9
    elif nature == "Rash":
        nature_dict['spatk'] = 1.1
        nature_dict['spdef'] = 0.9
    elif nature == "Calm":
        nature_dict['spdef'] = 1.1
        nature_dict['patk'] = 0.9
    elif nature == "Gentle":
        nature_dict['spdef'] = 1.1
        nature_dict['pdef'] = 0.9
    elif nature == "Sassy":
        nature_dict['spdef'] = 1.1
        nature_dict['spe'] = 0.9
    elif nature == "Careful":
        nature_dict['spdef'] = 1.1
        nature_dict['spatk'] = 0.9
    return nature_dict

#create chrome webdriver and navigate to smogon xy

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get("https://www.smogon.com/dex/sm/pokemon/")

#get links of pokemon sets
j = 184
links = set()
#935
for i in range(935):
    time.sleep(1.25)
    driver.execute_script("window.scrollTo(0, " + str(j) + ")") 
    element = driver.find_element_by_class_name("PokemonAltRow-name")
    link = str(element.find_element_by_tag_name("a").get_attribute('href'))
    links.add(link)
    j += 36.8
 
#get extra links
time.sleep(1)
li = driver.find_elements_by_class_name("PokemonAltRow")
for element in li:
    time.sleep(.5)
    link = str(element.find_element_by_tag_name("a").get_attribute('href'))
    links.add(link)
 
#sort in alpha order
links = sorted(links, key=str.lower)
 
#write sets to txt files
n = 0
for link in links:
    driver.get(link)
    try:
        tierlist = driver.find_element_by_class_name("PokemonPage-StrategySelector")
    except:
        continue
    ls = tierlist.find_elements_by_tag_name("a")
    tierlinks = [driver.current_url]
    tiers = [tierlist.find_element_by_class_name("is-selected").text]
    for l in ls:
        tierlinks.append(l.get_attribute('href'))
        tiers.append(l.text)
    t = 0
    for tierlink in tierlinks:
        driver.get(tierlink)
        buttons = driver.find_elements_by_class_name("ExportButton")
        i = 0
        headers = []
        for b in buttons:
            b.click()
            p = b.find_element_by_xpath("..")
            header = p.find_element_by_tag_name("h1").get_attribute('textContent')
            headers.append(header)
        sets = driver.find_elements_by_tag_name("textarea")
        for s in sets:
            text = open("s" + str(n) + ".txt", "w")
            text.write(s.text)
            text.write("\n")
            text.write(headers[i])
            text.write("\n")
            text.write(tiers[t])
            text.close()
            i+=1
            n+=1
            time.sleep(1)
        t+=1

driver.quit()

#create list of all pokemon and movesets
masterlist = []
oldname = ""
#read each moveset file
for j in range(n):
    text = open("s" + str(j) + ".txt", "r")
    txt = text.read()
    at = txt.find("@")
    nl1 = txt.find("\n")
    if at > 0:
        name = txt[0:at].strip()
        item = txt[at + 1:nl1].strip()
    else:
        name = txt[0:nl1].strip()
        item = ""
    abilityIndex = txt.find("Ability: ")
    nl2 = txt.find("\n", abilityIndex)
    ability = txt[abilityIndex + 9:nl2].strip()
    nl3 = txt.find("\n", nl2 + 1)
    evList = txt[nl2:nl3].split()
    evs = {"hp": 0,
           "ptk": 0,
           "pdef": 0,
           "spatk": 0,
           "spdef": 0,
           "spe": 0
           }
    if "HP" in evList:
        hpIndex = evList.index("HP")
    if "Atk" in evList:
        atkIndex = evList.index("Atk")
    if "Def" in evList:
        defIndex = evList.index("Def")
    if "SpA" in evList:
        spaIndex = evList.index("SpA")
    if "SpD" in evList:
        spdIndex = evList.index("SpD")
    if "Spe" in evList:
        speIndex = evList.index("Spe")
    if "hpIndex" in locals():
        evs["hp"] = int(evList[hpIndex - 1])
        del hpIndex
    if "atkIndex" in locals():
        evs["patk"] = int(evList[atkIndex - 1])
        del atkIndex
    if "defIndex" in locals():
        evs["pdef"] = int(evList[defIndex - 1])   
        del defIndex 
    if "spaIndex" in locals():
        evs["spatk"] = int(evList[spaIndex - 1])    
        del spaIndex
    if "spdIndex" in locals():
        evs["spdef"] = int(evList[spdIndex - 1])  
        del spdIndex  
    if "speIndex" in locals():
        evs["spe"] = int(evList[speIndex - 1])  
        del speIndex
    natureSpace = txt.find(" ", nl3)
    nature = txt[nl3:natureSpace].strip()
    natureD = convertNature(nature)
    m1 = txt.find("\n- ")
    m2 = txt.find("\n- ", m1 + 1)
    m3 = txt.find("\n- ", m2 + 1)
    m4 = txt.find("\n- ", m3 + 1)
    endM = txt.find("\n", m4 + 1)
    moves = []
    moves.append(txt[m1 + 3:m2])
    moves.append(txt[m2 + 3:m3])
    moves.append(txt[m3 + 3:m4])
    moves.append(txt[m4 + 3:endM])
    endLine = txt.find("\n", endM + 1)
    setName = txt[endM:endLine].strip()
    tier = txt[endLine:len(txt)].strip()
    moveset = {"ability": ability,
               "evs": evs,
               "item": item,
               "moves": moves,
               "name": setName,
               "nature": natureD,
               "tag": tier
               }
    if(name == oldname):
        masterlist[len(masterlist) - 1]["movesets"].append(moveset)
    else:
        pokedict = {"movesets": [], "name": "", "stats": {}, "typing": []}
        pokedict["name"] = name
        try:
            mon = Pokemon(name)
        except:
            print(str(j))
        pokedict["stats"] = mon.stats
        pokedict["typing"] = mon.typing
        pokedict["movesets"].append(moveset)
        masterlist.append(pokedict)
        oldname = name        

#dump list
s = json.dumps(masterlist, indent = 4)
open("poke.json","w").write(s)