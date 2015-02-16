import io,os,sys


def split(filename,numLines):
    list = []
    with open(filename,"r") as file:
        list = file.readlines()
    start = 0
    stop = 0
    numFiles = 1
    for id in list:
        if stop == numLines:
            with open(filename + str(numFiles),"w") as file:
                file.write("".join(list[start:stop]))
            start = stop
            numFiles = numFiles + 1
        stop = stop + 1
        
    #Last Remaining
    if start != stop:
        with open(filename + str(numFiles),"w") as file:
                file.write("".join(list[start:stop]))
split("seriesIDs.txt",10000)
                