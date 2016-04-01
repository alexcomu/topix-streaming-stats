__author__ = 'alexcomu'
import sys, json

def process(filename):
    result = []
    for i in range(6,22):
        result.append([])
    with open(filename, "r") as f:
        for line in f.readlines():
            splitted_line = line.split()
            day, slot = splitted_line[0].split("_")
            if int(day) > 5 and int(day) < 26:
                result[int(day)-6].append({"slot": slot, "value": splitted_line[1]})
    for idx, value in enumerate(result):
        check_range = [i for i in range(8)]
        for v in value:
            check_range.remove(int(v["slot"]))
        for tmp in check_range:
            result[idx].append({"slot": tmp, "value":0})
    print json.dumps(dict(values=result))



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Error, I need filename!"
        sys.exit()
    process(sys.argv[1])
