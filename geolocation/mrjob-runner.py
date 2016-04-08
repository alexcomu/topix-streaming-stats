__author__ = 'alexcomu'
from from_ip_to_geo import MREvaluateGeolocation
import json, logging

logging.basicConfig(level=logging.INFO)


mr_job = MREvaluateGeolocation()
mr_job.stdin = open('/CSV-PATH.csv')

result = {}
with mr_job.make_runner() as runner:
    runner.run()
    for line in runner.stream_output():
        country, occurrences = mr_job.parse_output_line(line)
        result[country] = occurrences

print json.dumps(result)
