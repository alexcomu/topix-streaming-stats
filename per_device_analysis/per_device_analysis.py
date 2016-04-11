__author__ = 'alexcomu'
from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime as dt

# Data Format
# film;  1454331524;  995823735;  213.61.32.110; 3;            1580;          0;            wowza02-f;    _definst_;  stream_name.mp4
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

class MRTransmissionTimePerDevice(MRJob):
    '''
    For each year and for each device calculate the avarage transmission time
    '''

    def steps(self):
        return [
            MRStep(mapper=self.year_device_seconds_mapper, reducer=self.avarage_reducer)
        ]

    def year_device_seconds_mapper(self, _, line):
        (app_name, timestamp_start, session_id,
         client_ip, length_stream, kbyte_transf,
         client_type, server_name, wowza_instance, stream_name) = line.split(";")
        timestamp_start_dt_ver = dt.fromtimestamp(int(timestamp_start))
        if timestamp_start_dt_ver.year != 2016:
            yield (timestamp_start_dt_ver.year, client_type), int(length_stream)

    def avarage_reducer(self, key, length_values):
        yield key, sum(length_values)


class MRAvarageTransmissionTime(MRJob):
    '''
    For each year and for each device calculate the avarage transmission time
    '''

    def steps(self):
        return [
            MRStep(mapper=self.year_device_seconds_mapper, reducer=self.avarage_reducer)
        ]

    def year_device_seconds_mapper(self, _, line):
        (app_name, timestamp_start, session_id,
         client_ip, length_stream, kbyte_transf,
         client_type, server_name, wowza_instance, stream_name) = line.split(";")
        timestamp_start_dt_ver = dt.fromtimestamp(int(timestamp_start))
        if timestamp_start_dt_ver.year != 2016:
            yield (timestamp_start_dt_ver.year, client_type), int(length_stream)

    def avarage_reducer(self, key, length_values):
        total = 0
        count = 0
        for value in length_values:
            total += value
            count += 1
        yield key, (total/count)


class MRAvarageTimePerApp(MRJob):
    '''
    For each Application -> avarage time of connection
    '''


    def steps(self):
        return [
            MRStep(mapper=self.app_seconds_mapper, reducer=self.avarage_reducer)
        ]

    def app_seconds_mapper(self, _, line):
        (app_name, timestamp_start, session_id,
         client_ip, length_stream, kbyte_transf,
         client_type, server_name, wowza_instance, stream_name) = line.split(";")
        if app_name in ["berlinale_pkd", "berlinale_pke", "berlinale_rtd", "berlinale_rte"]:
            yield app_name, int(length_stream)

    def avarage_reducer(self, key, length_values):
        total = 0
        count = 0
        for value in length_values:
            total += value
            count += 1
        yield key, (total/count)


class MRAmountOfSeconds(MRJob):
    '''
    Sum of total amount of second of transmission
    '''

    def steps(self):
        return [
            MRStep(mapper=self.app_seconds_mapper, reducer=self.avarage_reducer)
        ]

    def app_seconds_mapper(self, _, line):
        (app_name, timestamp_start, session_id,
         client_ip, length_stream, kbyte_transf,
         client_type, server_name, wowza_instance, stream_name) = line.split(";")
        timestamp_start_dt_ver = dt.fromtimestamp(int(timestamp_start))
        if app_name in ["berlinale_pkd", "berlinale_pke", "berlinale_rtd", "berlinale_rte", "berlinale_rt"]:
            yield (timestamp_start_dt_ver.year, app_name), int(length_stream)

    def avarage_reducer(self, key, length_stream):
        yield key, sum(length_stream)


if __name__ == '__main__':
    MRTransmissionTimePerDevice.run()
