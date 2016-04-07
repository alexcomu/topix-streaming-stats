__author__ = 'alexcomu'
from stream_resolution_aggregator import MRTotalAmoutOfKybytesPerYear, MRSumIPNumber
import json, logging

logging.basicConfig(level=logging.INFO)

def readable_bytes(num, suffix='B'):
    for unit in ['Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

mr_job = MRSumIPNumber()
mr_job.stdin = open('../../berlinale_csv/berlinale_aggregated.csv')

result = {}
with mr_job.make_runner() as runner:
    runner.run()
    for line in runner.stream_output():
        # stream_type, kbytes = mr_job.parse_output_line(line)
        # result[stream_type] = readable_bytes(kbytes)
        year, ip = mr_job.parse_output_line(line)
        result[year] = ip

print json.dumps(result)
