__author__ = 'alexcomu'
from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime as dt

# Data Format
# berlinale_film;  1454331524;  995823735;  213.61.32.110; 3;            1580;          0;            wowza02-f;    _definst_;  2010_Heimatland_web.mp4
# app-name;        timestamp;   session-id; client-IP;     length(sec);  kbyte-transf;  client-type;  nome-server;  instance;   nome-stream;

def readable_bytes(num, suffix='B'):
    for unit in ['Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

class MRSumKbytesPerDeviceType(MRJob):
    '''
    Sum the total kybets transmitted per device each year
    '''

    def steps(self):
        return [
            MRStep(mapper=self.year_device_kbytes_aggregator, reducer=self.sum_bandwith)
        ]

    def year_device_kbytes_aggregator(self, _, line):
        (app_name, timestamp_start, session_id,
         client_ip, length_stream, kbyte_transf,
         client_type, server_name, wowza_instance, stream_name) = line.split(";")
        timestamp_start_dt_ver = dt.fromtimestamp(int(timestamp_start))
        if timestamp_start_dt_ver.year != "2016":
            yield (timestamp_start_dt_ver.year, client_type), int(kbyte_transf)

    def sum_bandwith(self, key, kbytes):
        yield key, readable_bytes(sum(kbytes))


class MRAvarageTransmissionTime(MRJob):
    '''
    For each year and for each device calculate the avarage transmission time
    '''


    



if __name__ == '__main__':
    MRSumKbytesPerDeviceType.run()
