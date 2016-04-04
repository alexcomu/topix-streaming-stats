__author__ = 'alexcomu'
import sys, json

def readable_bytes(num, suffix='B'):
    for unit in ['Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def process(filename):
    with open(filename, "r") as f:
        result = []
        data = json.load(f)
        days = [i for i in range(1, 30)]
        slots = [i for i in range(8)]
        for day in days:
            if str(day) in data.keys():
                tmp = []
                tot_kbytes = 0
                for slot in slots:
                    if str(slot) in data[str(day)]:
                        tot_kbytes += int(data[str(day)][str(slot)])
                print "\n### Day: ", day, "\t\t\tTot: ", readable_bytes(tot_kbytes)
                for slot in slots:
                    if str(slot) in data[str(day)]:
                        print "Slot",slot,"\t->\t",round((float(data[str(day)][str(slot)])*100)/tot_kbytes, 2),"%\t\t",readable_bytes(int(data[str(day)][str(slot)]))
                        tmp.append({"slot":slot, "perc": round((float(data[str(day)][str(slot)])*100)/tot_kbytes, 2), "bytes":readable_bytes(int(data[str(day)][str(slot)]))})
                    else:
                        print "Slot",slot,"\t->\t0\t\t0 %"
                        tmp.append({"slot": slot, "perc": 0, "bytes":0})
                result.append(tmp)
        # with open("aggregated_%s"%filename,"w") as write_f:
        #     write_f.write(json.dumps(result))




if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Error, I need filename!"
        sys.exit()
    process(sys.argv[1])
