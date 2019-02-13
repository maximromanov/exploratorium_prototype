import json, os
import time, re, sys, itertools
start = time.time()

# convert `desc`-tsv files into JSON

def converter(file):
    print(file)
    with open(file, "r", encoding="utf8") as f1:
        data = f1.read().split("\n")

        head = data[0].split("\t")
        #print(head)

        dic = {}
        for d in data[1:]:
            d = d.split("\t")
            if d[2] != "":
                count = 0
                dt = {}
                d[3] = d[3].replace(" ", "").split(",")
                for h in head:
                    dt[h] = d[count]
                    count += 1

                dic[d[0]] = dt
                
        with open(file+"Scheme.json","w",encoding='utf-8') as f9:
            json.dump(dic,f9,sort_keys=True, indent=4, ensure_ascii=False)


def processAll():
    lof = os.listdir(".")
    for f in lof:
        if f.endswith(".desc"):
            converter(f)

processAll()


end = time.time()
print("Processing time: {0:.2f} sec".format(end - start))
print("Tada!")
