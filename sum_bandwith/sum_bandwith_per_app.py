__author__ = 'alexcomu'
from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime as dt

# Data Format
# berlinale_film;  1454331524;  995823735;  213.61.32.110; 3;            1580;          0;            wowza02-f;    _definst_;  2010_Heimatland_web.mp4
# app-name;        timestamp;   session-id; client-IP;     length(sec);  kbyte-transf;  client-type;  nome-server;  instance;   nome-stream;

class MRSumBandwithPerApp(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_app, reducer=self.sum_bandwith),
            MRStep(mapper=self.order_by_name, reducer=self.order_result)
        ]

    def mapper_app(self, _, line):
        (app_name, timestamp_start, session_id,
         client_ip, length_stream, kbyte_transf,
         client_type, server_name, wowza_instance, stream_name) = line.split(";")
        timestamp_start_dt_ver = dt.fromtimestamp(int(timestamp_start))
        #yield app_name, int(kbyte_transf)
        yield "%s_%s" % (timestamp_start_dt_ver.year, app_name), int(kbyte_transf)

    def sum_bandwith(self, key, occurrences):
        yield key, sum(occurrences)

    def order_by_name(self, key, value):
        yield None, (key, value)

    def order_result(self, _, values):
        for value in values:
            yield value[0], value[1]

if __name__ == '__main__':
    MRSumBandwithPerApp.run()
