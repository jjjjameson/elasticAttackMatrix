import json

jsonFile = 'enabledRules.json'

def openJson(jsonFileName):
    f = open('enabledRules.json')
    mitreFile = json.load(f)['data']
    f.close()
    return mitreFile

def buildTacticMap(data):
    tacticMap = {}

    def parseTacticName(tacticName):
        parsedNameList = []
        for c in tacticName.lower():
            if c == ' ':
                parsedNameList.append('-')
            else:
                parsedNameList.append(c)
        return "".join(parsedNameList)
    
    if data is not None:
        for dataEntry in data:
            entryName = dataEntry['name']
            if 'params' not in dataEntry:
                continue
            for threatItem in dataEntry['params']['threat']:
                tacticName = parseTacticName(threatItem['tactic']['name'])
                if (tacticName not in tacticMap):
                    tacticMap[tacticName] = {}
                nameMap = tacticMap[tacticName]
                for technique in threatItem['technique']:
                    techniqueIdKey = technique['id']
                    if techniqueIdKey not in nameMap:
                        nameMap[techniqueIdKey] = {}
                    techniqueValue = nameMap[techniqueIdKey]
                    if "score" not in techniqueValue:
                        techniqueValue["score"] = 0
                    techniqueValue["score"]+=1
                    if "comment" not in techniqueValue:
                        techniqueValue["comment"] = entryName
                    else:
                        techniqueValue["comment"] = techniqueValue["comment"] + "\n" + entryName + ","
                    if 'subtechnique' not in technique:
                        continue
                    for subtechnique in technique['subtechnique']:
                        subtechniqueIdKey = subtechnique['id']
                        if subtechniqueIdKey not in nameMap:
                            nameMap[subtechniqueIdKey] = {}
                        subtechniqueValue = nameMap[subtechniqueIdKey]
                        if "score" not in subtechniqueValue:
                            subtechniqueValue["score"] = 0
                        subtechniqueValue["score"]+=1
                        if "comment" not in subtechniqueValue:
                            subtechniqueValue["comment"] = entryName
                        else:
                            subtechniqueValue["comment"] = subtechniqueValue["comment"] + "\n" + entryName + ","
    return tacticMap

def saveToJson(tacticMap):
    def containsIdAndTactic(techniqueId, tactic, jsonEntry):
        return techniqueId in jsonEntry.values() and tactic in jsonEntry.values()

    with open('blankNavigatorFile.json', 'r') as file:
        emptyMitreJson = json.load(file)

        for tactic in tacticMap:
            for techniqueId in tacticMap[tactic]:
                for jsonEntry in emptyMitreJson["techniques"]:
                    if containsIdAndTactic(techniqueId, tactic, jsonEntry):
                        techniqueValue = tacticMap[tactic][techniqueId]
                        jsonEntry['comment'] = jsonEntry['comment'] + techniqueValue["comment"]
                        jsonEntry['score'] = techniqueValue['score']

        newData = json.dumps(emptyMitreJson, indent=4)

    with open('elasticMap.json', 'w') as file:
        file.write(newData)

    print("Data Processing Complete")

def main():
    data = openJson(jsonFile)
    tacticMap = buildTacticMap(data)
    saveToJson(tacticMap)
main()