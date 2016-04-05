__author__ = 'alexcomu'
import sys, json

def process(filename):
    result = []
    for i in range(30):
        result.append([])
    with open(filename, "r") as f:
        for line in f.readlines():
            splitted_line = line.split()
            day, slot = splitted_line[0].split("_")
            result[int(day)].append({"slot": slot, "value": splitted_line[1]})
            # if int(day) > 5 and int(day) < 28:
            #     print result
            #     result[int(day)-6].append({"slot": slot, "value": splitted_line[1]})
    for idx, value in enumerate(result):
        check_range = [i for i in range(8)]
        for v in value:
            check_range.remove(int(v["slot"]))
        for tmp in check_range:
            result[idx].append({"slot": tmp, "value":0})

    cont = 0
    check_range = [i for i in range(8)]
    response = []
    for day in result:
        for idx in check_range:
            for step in day:
                if int(step["slot"]) == idx:
                    response.append({"x": cont, "y": step["value"]})
                    cont += 1
    print json.dumps(response)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Error, I need filename!"
        sys.exit()
    process(sys.argv[1])
