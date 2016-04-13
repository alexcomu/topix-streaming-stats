# TOP-IX MapReduce for Wowza Logs

## Data Format

Data are aggregated with this specific format:

    $ app-name;1454331524;995823735;213.61.32.110;a;1580;0;wowza02-f;_definst_;wowza_app
    $ app-name;timestamp-start;session-id;client-IP;durata(sec);kbyte-trasferiti;client-type;nome-server;istanza;nome-stream;

## How to run Viz

Where you find an HTML page use Python simple server to see the viz:

    $ python -m SimpleHTTPServer

## Jobs

There are multiple jobs on MapReduce to analyze raw log from Wowza Streaming servers. Here an abstract.

### Sum Bandwith

The goal is to count, per each year / application the total amount of kbytes transmitted.
There are two steps, the first one count the total kbytes and the second is used to order the results.

### Sum Bandwit per day

There are 2 different jobs:

* MRSumBandwithPerDay: Total amount of kbytes per day
* MRSumBandwithPerDayPerSlot: Total amount of kbytes per day per slot time

### Stream resolution aggregator on 2016

There are 3 different jobs:

* MRStreamAggregator: For each stream name, sum the kbytes
* MRTotalAmoutOfKybytesPerYear: Total amount of kbytes transferred for all the valid apps per year
* MRSumIPNumber: Count IP Amount


### Per device analysis

There are 3 different jobs:

* MRSumKbytesPerDeviceType: Sum the total kbytes transmitted per device each year
* MRTransmissionTimePerDevice: For each year and for each device calculate the avarage transmission time
* MRAvarageTransmissionTime: For each year and for each device calculate the avarage transmission time
* MRAvarageTimePerApp: For each Application -> avarage time of connection
* MRAmountOfSeconds: Sum of total amount of second of transmission
* MRAmountOfSecondsPerYear: Total of seconds for 2016 transmissions

### Users per seconds

This job is used to calculate the amount of users connected at the same time in a given time slot. For example I'm calculating the total amount of people per second during the time slot *2016-02-11 18:00:00* / *2016-02-11 20:00:00*.

The result will be "timestamp" "user number".

### Geolocation

The goal is to geolocate each request and return the total amount of connections per country. I'm using a my own service to geolocate the IP Addresses.
