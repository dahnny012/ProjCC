def padNum(number, characters):
	return "0"*(characters - len(str(number))) + str(number)
	
	
def merge(filename,start,end):
    for i in range(start,end+1):
        print(filename+padNum(i,3)+".csv")
        with open('merged.csv', 'a') as outfile:
            with open(filename+padNum(i,3)+".csv") as infile:
                outfile.write(infile.read())

merge("uniqueSeries",1,14)
