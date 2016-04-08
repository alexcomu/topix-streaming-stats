__author__ = 'alexcomu'
from per_device_analysis import MRSumKbytesPerDeviceType
import json, logging

logging.basicConfig(level=logging.INFO)


mr_job = MRSumKbytesPerDeviceType()
mr_job.stdin = open('../../MY.csv')

result = {}
with mr_job.make_runner() as runner:
    runner.run()
    for line in runner.stream_output():
        app_name, kbyte_transf = mr_job.parse_output_line(line)
        result[app_name] = kbyte_transf
