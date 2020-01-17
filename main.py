import re

def getRegex(pattern):
    #pattern =   "{P}1-{PKRHW}2-[VLSWFNQ]3-[ILTYWFN]4-[FIY]5-{PKRH}6-F(3)-218-F(12)-F(128)-X(3)-X(1,3)-X(1,12)"

    for i in range(0, len(pattern)):
        if(pattern[i].isnumeric()):
            if(pattern[i] == pattern[-1:]):
                pattern = pattern[0:i]
                break
            elif(not (((pattern[i-1] == "(") or (pattern[i-1] == ",") or (pattern[i-1].isnumeric())) and ((pattern[i+1] == ")") or (pattern[i+1] == ",") or (pattern[i+1].isnumeric())))):
                newPattern = pattern[0:i] + pattern[i+1:]
                pattern = newPattern + "!"
    pattern = pattern.replace("!","")
    regex = ""

    patternParts = pattern.split("-")
    for part in patternParts:
        if(part.isnumeric()):
            continue
        allowedParts = {"G","A","V","L","I","P","F","Y","C","M","H","K","R","W","S","T","D","E","N","Q","B","Z"}
        allowedPartsStr = "GAVLIPFYCMHKRWSTDENQBZ"
        regexPart = "("
        if(part[0] == "{" and part[-1:] == "}"):
            part = part.replace("{","")
            part = part.replace("}","")
            disallowedBases = list(part)
            for base in disallowedBases:
                allowedParts.remove(base)
            regexPart = regexPart + "["
            for base in allowedParts:
                regexPart = regexPart + base
            regexPart = regexPart + "]"

        elif(part[0] == "[" and part[-1:] == "]"):
            part = part.replace("[", "")
            part = part.replace("]", "")
            allowedBases = list(part)
            regexPart = regexPart + "["
            for base in allowedBases:
                regexPart = regexPart + base
            regexPart = regexPart + "]"

        elif(allowedPartsStr.find(part[0]) != -1):
            regexPart = regexPart + "["
            if(part[1] == "(" and part[-1:] == ")"):
                regexPart = regexPart + part[0] + "]{"
                part = part.replace("(","")
                part = part.replace(")","")
                regexPart = regexPart + part[1:] + "}"
            else:
                regexPart = regexPart + part[0] + "]"

        elif(part[0] == "X"):
            regexPart = regexPart + "["
            if(len(part) == 1):
                regexPart = regexPart + part[0] + "]"
            else:
                if(part[1] == "(" and part[-1:] == ")"):
                    if(part.find(",") == -1):
                        regexPart = regexPart + part[0] + "]{"
                        part = part.replace("(","")
                        part = part.replace(")","")
                        regexPart = regexPart + part[1:] + "}"
                    else:
                        regexPart = regexPart + part[0] + "]{"
                        part = part.replace("(","")
                        part = part.replace(")","")
                        part = part.replace("X","")
                        regexPart = regexPart + part + "}"

        regexPart = regexPart + ")"
        regex = regex + regexPart
        
    return regex

prositePattern = "{P}1-{PKRHW}2-[VLSWFNQ]3-[ILTYWFN]4-[FIY]5-{PKRH}6-F(3)-218-F(12)-F(128)-X(3)-X(1,3)-X(1,12)"
reg = getRegex(prositePattern)
print("Prosite pattern: " + prositePattern)
print("Generated regex: " + reg)
