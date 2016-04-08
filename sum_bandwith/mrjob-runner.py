__author__ = 'alexcomu'
from sum_bandwith_per_app import MRSumBandwithPerApp
import json, logging

logging.basicConfig(level=logging.INFO)


mr_job = MRSumBandwithPerApp()
mr_job.stdin = open('/MY.csv')

result = {}
with mr_job.make_runner() as runner:
    runner.run()
    for line in runner.stream_output():
        app_name, kbyte_transf = mr_job.parse_output_line(line)
        result[app_name] = kbyte_transf

print json.dumps(result)
