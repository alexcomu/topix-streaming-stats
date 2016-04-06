__author__ = 'alexcomu'
from evaluate_hour import MREvaluateHour
import json, logging

logging.basicConfig(level=logging.INFO)


mr_job = MREvaluateHour()
mr_job.stdin = open('../../berlinale_csv/2016_berlinale.csv')

result = {}
keys = []
values = []
with mr_job.make_runner() as runner:
    runner.run()
    for line in runner.stream_output():
        timestamp, occurrences = mr_job.parse_output_line(line)
        # print "%s\t%s" % (timestamp, occurrences)
        result[timestamp] = occurrences
        keys.append(timestamp)
        values.append(occurrences)

print json.dumps(result)
with open("viz/keys.json", "w") as f:
    f.write(json.dumps(keys))
with open("viz/values.json", "w") as f:
    f.write(json.dumps(values))

