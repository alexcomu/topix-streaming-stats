__author__ = 'alexcomu'
from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime as dt
import time
from mrjob.protocol import RawProtocol, JSONValueProtocol

class MREvaluateHour(MRJob):

    start = dt.strptime("2016-02-11 18:00:00", "%Y-%m-%d %H:%M:%S")
    end = dt.strptime("2016-02-11 20:00:00", "%Y-%m-%d %H:%M:%S")
    timestamp_start = None
    timestamp_end = None

    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_init,
                   mapper=self.mapper_seconds,
                   reducer=self.sum_aggregation)
        ]

    def mapper_init(self):
        self.timestamp_start = time.mktime(self.start.timetuple())
        self.timestamp_end = time.mktime(self.end.timetuple())

    def mapper_seconds(self, _, line):
        (app_name, timestamp_start, session_id,
         client_ip, length_stream, kbyte_transf,
         client_type, server_name, wowza_instance, stream_name) = line.split(";")
        timestamp_start = int(timestamp_start)
        length_stream = int(length_stream)
        if timestamp_start > self.timestamp_start and timestamp_start+length_stream < self.timestamp_end:
            for i in xrange(length_stream+1):
                yield timestamp_start+i, 1


    def sum_aggregation(self, second, occurrences):
        yield second, sum(occurrences)