__author__ = 'alexcomu'
from mrjob.job import MRJob
from mrjob.step import MRStep

range_map = {"max": "", "min": "", "file": ""}


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

        '''
        Invece che leggere dal giga file, ne faccio tanti piu piccoli e li mappo
        in modo che se cerco un IP faccio un controllo, sta in un range? se si cerca nel file XYZ
        Altrimenti guarda il range dopo e cerca di conseguenza

        Creo un dict con il mapping dei range e con il puntatore al file da usare per cercare
        '''

        with open("/work/streaming-stats/scripts/geolocation/ip2location.csv", "r") as f:
            for line in f.readlines():
                splitted = line.split(",")
                range1, range2 = splitted[0:2]
                if decimal_ip > int(range1[1:-1]) and decimal_ip < int(range2[1:-1]):
                    country = splitted[2][1:-1]
                    if country in self.valid_region:
                        yield country, 1
                    else:
                        yield "OTHER", 1
                    break

    def sum_aggregation(self, country, occurrences):
        yield country, sum(occurrences)


if __name__ == '__main__':
    MREvaluateGeolocation.run()