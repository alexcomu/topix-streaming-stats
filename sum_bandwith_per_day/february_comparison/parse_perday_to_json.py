__author__ = 'alexcomu'
import sys, json

def process(filename):
    result = []
    with open(filename, "r") as f:
        for line in f.readlines():
            day, value = line.split()
            result.append({"x":int(day), "y": value})
        print json.dumps(result)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Error, I need filename!"
        sys.exit()
    process(sys.argv[1])
