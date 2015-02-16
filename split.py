import io,os,sys,re

def padNum(number, characters):
	return "0"*(characters - len(str(number))) + str(number)

def split(filename,numLines):
    list = []
    numLines = int(numLines)
    with open(filename,"r") as file:
        list = file.readlines()
        
    extRegex = re.compile('\.[A-Za-z]+$', re.IGNORECASE)
    fileExt = extRegex.search(filename)
    fileExt = fileExt.group(0)
    filename = extRegex.sub('', filename)
    
    start = 0
    stop = 0
    numFiles = 1
    for id in list:
        if stop%numLines == numLines-1:
            with open(filename + padNum(numFiles, 3) + fileExt,"w") as file:
                file.write("".join(list[start:stop]))
            start = stop
            numFiles = numFiles + 1
        stop = stop + 1
        
    #Last Remaining
    if start != stop:
        with open(filename + padNum(numFiles, 3) + fileExt,"w") as file:
                file.write("".join(list[start:stop]))

filename = sys.argv[1]
numLines = sys.argv[2]

split(filename, numLines)
