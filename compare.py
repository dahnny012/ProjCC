def compare(baseFile,generatedFile):
    map1 = {}
    map2 = {}
    
    base = []
    generated = []
    
    with open(baseFile,"r") as input1:
        base = input1.readlines()
    with open(generatedFile,"r") as input2:
        generated = input2.readlines()
    for id in base:
        map1[id] = id
    for id in generated:
        map2[id] = id
    with open("missing_"+generatedFile,"w") as diff:
        for key in map1:
            if key not in map2:
                diff.write(key)


compare("seriesIDs001.txt","seriesIDs001.log")