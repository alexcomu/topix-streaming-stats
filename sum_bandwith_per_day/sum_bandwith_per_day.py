__author__ = 'alexcomu'
from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime as dt
from mrjob.protocol import RawProtocol, JSONValueProtocol

# Data Format
# berlinale_film;  1454331524;  995823735;  213.61.32.110; 3;            1580;          0;            wowza02-f;    _definst_;  2010_Heimatland_web.mp4
# app-name;        timestamp;   session-id; client-IP;     length(sec);  kbyte-transf;  client-type;  nome-server;  instance;   nome-stream;

range_values = [10, 12, 14, 16, 18, 20, 22, 24]

class MRSumBandwithPerDayPerSlot(MRJob):

    OUTPUT_PROTOCOL = RawProtocol

    def steps(self):
        return [
            MRStep(mapper=self.mapper_app, reducer=self.sum_bandwith)
        ]

    def mapper_app(self, _, line):
        (app_name, timestamp_start, session_id,
         client_ip, length_stream, kbyte_transf,
         client_type, server_name, wowza_instance, stream_name) = line.split(";")
        timestamp_start_dt_ver = dt.fromtimestamp(int(timestamp_start))
        for idx, value in enumerate(range_values):
            if timestamp_start_dt_ver.hour < value:
                yield "%s_%s" % (timestamp_start_dt_ver.day, idx), int(kbyte_transf)
                break

    def sum_bandwith(self, key, occurrences):
        yield key, str(sum(occurrences))


class MRSumBandwithPerDay(MRJob):

    OUTPUT_PROTOCOL = RawProtocol

    def steps(self):
        return [
            MRStep(mapper=self.mapper_app, reducer=self.sum_bandwith)
        ]

    def mapper_app(self, _, line):
        (app_name, timestamp_start, session_id,
         client_ip, length_stream, kbyte_transf,
         client_type, server_name, wowza_instance, stream_name) = line.split(";")
        timestamp_start_dt_ver = dt.fromtimestamp(int(timestamp_start))
        if timestamp_start_dt_ver.day<10:
            yield "0%s" % (timestamp_start_dt_ver.day), int(kbyte_transf)
        else:
            yield str(timestamp_start_dt_ver.day), int(kbyte_transf)

    def sum_bandwith(self, key, occurrences):
        yield key, str(sum(occurrences))

if __name__ == '__main__':
    MRSumBandwithPerDay.run()
