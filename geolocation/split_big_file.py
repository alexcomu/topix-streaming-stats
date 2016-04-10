__author__ = 'alexcomu'

row_range = 200000
cont = 0
base_name = "result/%s_ip2location_split.csv"

buffer = []

with open('ip2location.csv', 'r') as f:
    for line in f.readlines():
        buffer.append(line)
        if len(buffer) == row_range:
            with open(base_name % cont, "w") as f:
                for value in buffer:
                    f.write(value)
            cont += 1
            buffer = []