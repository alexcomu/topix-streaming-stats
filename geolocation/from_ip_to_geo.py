__author__ = 'alexcomu'
from mrjob.job import MRJob
from mrjob.step import MRStep
import requests

class MREvaluateGeolocation(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.ip_mapper,
                   reducer=self.sum_aggregation)
        ]

    def ip_mapper(self, _, line):
        (app_name, timestamp_start, session_id,
         client_ip, length_stream, kbyte_transf,
         client_type, server_name, wowza_instance, stream_name) = line.split(";")
        resp = requests.get("http://geoip.top-ix.org/"+client_ip)
        if resp.status_code == 200:
            resp_json = resp.json()
            if resp_json["status"] == 200:
                yield resp_json["geoip"]["country_code"], 1


    def sum_aggregation(self, country, occurrences):
        yield country, sum(occurrences)


if __name__ == '__main__':
    MREvaluateGeolocation.run()
