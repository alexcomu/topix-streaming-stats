__author__ = 'alexcomu'
from mrjob.job import MRJob
from mrjob.step import MRStep


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