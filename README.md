# TOP-IX MapReduce for Wowza Logs

## Data Format

Data are aggregated with this specific format:

    $ app-name;1454331524;995823735;213.61.32.110;a;1580;0;wowza02-f;_definst_;wowza_app
    $ app-name;timestamp-start;session-id;client-IP;durata(sec);kbyte-trasferiti;client-type;nome-server;istanza;nome-stream;

## How to run
    
Where you find an HTML page use Python simple server to see the viz:

    $ python -m SimpleHTTPServer

