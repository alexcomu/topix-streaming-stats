__author__ = 'alexcomu'
from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime as dt

class MRStreamAggregator(MRJob):
    '''
    For each stream name, sum the kbytes
    '''

    stream_type = ["streaming_out_720p", "streaming_out_540p",
                   "streaming_out_360p", "streaming_out_240p",
                   "streaming_out_mobile"]

    valid_app = ["berlinale_pkd", "berlinale_pke", "berlinale_rtd", "berlinale_rte"]

    def steps(self):
        return [
            MRStep(mapper=self.stream_mapper,
                   reducer=self.sum_aggregation)
        ]

    def stream_mapper(self, _, line):
        (app_name, timestamp_start, session_id,
         client_ip, length_stream, kbyte_transf,
         client_type, server_name, wowza_instance, stream_name) = line.split(";")
        if stream_name in self.stream_type and app_name in self.valid_app:
            yield stream_name, int(kbyte_transf)


    def sum_aggregation(self, stream_type, kbytes):
        yield stream_type, sum(kbytes)


class MRTotalAmoutOfKybytesPerYear(MRJob):
    '''
    Total amount of kbytes transferred for all the valid apps per year
    '''

    valid_app = ["berlinale_pkd", "berlinale_pke", "berlinale_rtd", "berlinale_rte"]

    def steps(self):
        return [
            MRStep(mapper=self.stream_mapper,
                   reducer=self.sum_aggregation)
        ]

    def stream_mapper(self, _, line):
        (app_name, timestamp_start, session_id,
         client_ip, length_stream, kbyte_transf,
         client_type, server_name, wowza_instance, stream_name) = line.split(";")
        timestamp_start_dt_ver = dt.fromtimestamp(int(timestamp_start))

        if app_name in self.valid_app:
            yield timestamp_start_dt_ver.year, int(kbyte_transf)

    def sum_aggregation(self, year, kbytes):
        yield year, sum(kbytes)


class MRSumIPNumber(MRJob):
    '''
    Count IP Amount
    '''

    valid_app = ["berlinale_pkd", "berlinale_pke", "berlinale_rtd", "berlinale_rte"]

    def steps(self):
        return [
            MRStep(mapper=self.ip_mapper,
                   reducer=self.year_normalization),
            MRStep(reducer=self.year_count)
        ]

    def ip_mapper(self, _, line):
        (app_name, timestamp_start, session_id,
         client_ip, length_stream, kbyte_transf,
         client_type, server_name, wowza_instance, stream_name) = line.split(";")
        timestamp_start_dt_ver = dt.fromtimestamp(int(timestamp_start))
        if app_name in self.valid_app and int(length_stream) > 10:
            yield client_ip, timestamp_start_dt_ver.year

    def year_normalization(self, client_ip, years):
        for year in years:
            yield year, client_ip

    def year_count(self, year, client_ips):
        total = 0
        for ip in client_ips:
            total += 1
        yield year, total


