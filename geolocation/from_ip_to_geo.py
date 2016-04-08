__author__ = 'alexcomu'
from mrjob.job import MRJob
from mrjob.step import MRStep


class MREvaluateGeolocation(MRJob):

    valid_region = ["IT", "DE", "FR", "GB", "ES", "BE", "NL", "PL", "IE", "DK"]

    def from_ip_to_decimal(self, ip):
        parts = ip.split('.')
        return (int(parts[0]) << 24) + (int(parts[1]) << 16) + (int(parts[2]) << 8) + int(parts[3])

    def steps(self):
        return [
            MRStep(mapper=self.ip_mapper,
                   reducer=self.sum_aggregation)
        ]

    def ip_mapper(self, _, line):
        (app_name, timestamp_start, session_id,
         client_ip, length_stream, kbyte_transf,
         client_type, server_name, wowza_instance, stream_name) = line.split(";")
        decimal_ip = self.from_ip_to_decimal(client_ip)

        # cerco il range di IP -> Chiamo un API?
        # controllo se rientra nella valid o nelle other
        # mappo la country, 1

        yield 1, 1


    def sum_aggregation(self, country, occurrences):
        yield country, sum(occurrences)