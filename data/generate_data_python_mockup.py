from os.path import join, getsize
import time, re, sys, itertools, json
start = time.time()

# picking a descriptor
val = "الواعظ"

def normalizeArabic(text):
    text = re.sub("[إأٱآا]", "ا", text)
    #text = re.sub("ى", "ي", text)
    #text = re.sub("(ؤ)", "و", text)
    #text = re.sub("(ئ)", "ي", text)
    #text = re.sub("(ة)", "ه", text)
    return(text)


def loadRegions():
    with open("./temp/regions.json", encoding="utf8") as json_data:
        d = json.load(json_data)
        regions = {}
        for k,v in d.items():
            key = v["region_code"]
            val = v
            regions[key] = val
        return(d)

def loadDesc(file):
    with open(file, encoding="utf8") as json_data:
        d = json.load(json_data)
##        for k,v in d.items():
##            print(k)
##            print(v)
##            input()
        return(d)



def loadGeoJSON(file):
    with open(file, encoding="utf8") as json_data:
        data = json.load(json_data)
        spelled = {} # spelled
        uris    = {} # uris as keys
        
        for f in data["features"]:
            keySpe = f["archive"]["cornuData"]["toponym_arabic"] # this should be a URI, not a spelled version, of course
            keySpe = normalizeArabic(keySpe)
            keyUri = f["archive"]["cornuData"]["cornu_URI"]
            val = (f["archive"]["cornuData"])
##            print(keySpe)
##            print(keyUri)
##            print(val)
##            input()
            spelled[keySpe] = val
            uris[keyUri] = val
            
    return(uris, spelled)

regions = loadRegions()         
placesUris, placesSpel = loadGeoJSON("./temp/places_new_structure.geojson")
descDic = loadDesc("0748Dhahabi.TarikhIslam.JK007088-ara1.descScheme.json")

def calc_geographicalPresence(dataFile, val):
    print("#########"* 10)
    print("### STATS FOR: %s" % val)
    print("#########"* 10)
    
    regions = {}
    settlem = {}
    with open(dataFile, "r", encoding="utf8") as f1:
        data = f1.read().split("\n")

        # general dataList
        dataList = []
        for d in data[1:]:
            dataList.append(d.split("\t"))

        # getting IDs
        idList = []
        for d in dataList:
            if d[1] == val:
                idList.append(d[0])

        # getting all data for IDs
        valData = []
        for d in dataList:
            if d[0] in idList:
                valData.append(d)
                #input(valData)

        # building geoTable: # ID, SETTLEMENT, REGION, R/V
        geoTable = []
        for v in valData:
            if v[2] == "desc":
                if v[1] in descDic:
                    if re.search("[A-Z]+_\d\d\d\w\d\d\d\w_\w", descDic[v[1]]["TOP_URI"]):
                        var = descDic[v[1]]
                        temp = placesUris[var["TOP_URI"]]
                        #input(temp)
                        line = [v[0], temp["toponym_translit"], temp["region_spelled"], "resident"]
                        geoTable.append(line)
            elif v[2] == "topo":
                if v[1] in placesSpel:
                    temp = placesSpel[v[1]]
                    line = [v[0], temp["toponym_translit"], temp["region_spelled"], "visitor"]
                    geoTable.append(line)
            else:
                pass # the remaining should be dates (`yede`)

        # now, counting:

        # regions
        reg_All = []
        reg_Res = []

        # settlements
        set_All = []
        set_Res = []

        for g in geoTable:
            regV = "\t".join([g[0], g[2]])
            setV = "\t".join([g[0], g[2]+": "+g[1]])
            if g[3] == "resident":
                reg_Res.append(regV)
                set_Res.append(setV)
                reg_All.append(regV)
                set_All.append(setV)

            else:
                reg_All.append(regV)
                set_All.append(setV)

        reg_Res = list(set(reg_Res))
        set_Res = list(set(set_Res))
        reg_All = list(set(reg_All))
        set_All = list(set(set_All))

        # res and all in Regions:
        print()
        print("#########"* 10)
        print("### REGIONAL STATISTICS #####")
        print("#########"* 10)
        print()
        regRes = listIntoDic(reg_Res)
        regAll = listIntoDic(reg_All)

        for k in sorted(regAll):
            if k in regRes:
                count = regRes[k]
            else:
                count = 0
            print("\n%s\n\tAll:\t%d;\tRes:\t%d;\tVis:\t%s" % (k, regAll[k], count, (regAll[k]-count)))

            
        # res and all in Settlements:
        print("#########"* 10)
        print("### SETTLEMENT STATISTICS #####")
        print("#########"* 10)
        print()
        regRes = listIntoDic(set_Res)
        regAll = listIntoDic(set_All)
        for k in sorted(regAll):
            if k in regRes:
                count = regRes[k]
            else:
                count = 0
            print("\n%s\n\tAll:\t%d;\tRes:\t%d;\tVis:\t%s" % (k, regAll[k], count, (regAll[k]-count)))
        
    
                
def listIntoDic(listVar):
    dicVar = {}
    for l in listVar:
        l = l.split("\t")
        if l[1] in dicVar:
            dicVar[l[1]] += 1
        else:
            dicVar[l[1]]  = 1
    return(dicVar)
        
        
calc_geographicalPresence("0748Dhahabi.TarikhIslam.JK007088-ara1.dataUni", val)


end = time.time()
print("Processing time: {0:.2f} sec".format(end - start))
print("Tada!")


import itertools
itertools.permutations([1, 2, 3])
