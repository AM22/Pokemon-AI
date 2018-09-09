from selenium import webdriver
import time
import json
from gamestateEdited import Pokemon

#create chrome webdriver and navigate to smogon xy
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get("https://www.smogon.com/dex/xy/pokemon/")

#get links of pokemon sets
j = 184
links = set()
for i in range(900):
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, " + str(j) + ")") 
    element = driver.find_element_by_class_name("PokemonAltRow-name")
    link = str(element.find_element_by_tag_name("a").get_attribute('href'))
    links.add(link)
    j += 36.8

#get extra links
li = driver.find_elements_by_class_name("PokemonAltRow")
for element in li:
    link = str(element.find_element_by_tag_name("a").get_attribute('href'))
    links.add(link)

#sort in alpha order
links = sorted(links, key=str.lower)

#write sets to txt files
i = 0
for link in links:
    driver.get(link)
    buttons = driver.find_elements_by_class_name("ExportButton")
    headers = []
    for b in buttons:
        b.click()
        p = driver.find_elements_by_xpath("..")
        header = p.find_elements_by_tag_name("h1").text
        headers.append(header)
    sets = driver.find_elements_by_tag_name("textarea")
    for s in sets:
        text = open("s" + str(i) + ".txt", "w")
        text.write(s.text)
        text.write("\n")
        text.write(headers[i])
        text.close()
        i+=1
        time.sleep(1)

#create list of all pokemon and movesets
masterList = []
oldname = ""
#read each moveset file
for j in range(i):
    text = open("s" + str(j) + ".txt", "r")
    txt = text.read()
    at = txt.find("@")
    name = txt[0:at].strip()
    nl1 = txt.find("\n")
    item = txt[at + 1:nl1].strip()
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
    if "atkIndex" in locals():
        evs["patk"] = int(evList[atkIndex - 1])
    if "defIndex" in locals():
        evs["pdef"] = int(evList[defIndex - 1])    
    if "spaIndex" in locals():
        evs["spatk"] = int(evList[spaIndex - 1])    
    if "spdIndex" in locals():
        evs["spdef"] = int(evList[spdIndex - 1])    
    if "speIndex" in locals():
        evs["spe"] = int(evList[speIndex - 1])  
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
    setName = txt[endM:len(txt)].strip()
    moveset = {"ability": ability,
               "evs": evs,
               "item": item,
               "moves": moves,
               "name": setName,
               "nature": natureD
               }
    if(name == oldname):
        masterlist[len(masterlist) - 1]["movesets"].append(moveset)
    else:
        pokedict = {"movesets": [], "name": "", "stats": {}, "typing": []}
        pokedict["name"] = name
        mon = Pokemon(name)
        pokedict["stats"] = mon.stats
        pokedict["typing"] = mon.typing
        pokedict["movesets"].append(moveset)
        masterlist.append(pokedict)
        oldname = name        

#dump list
with open('poke.json', 'w') as js:
    json.dump(masterlist, js)
    
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
