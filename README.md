# Server-Client-File-Transfer
Description:
------------------------------------------------------------------------------------------------------------------------
Simple server and client made in python with sockets. The server will send the client a sentence in either English, Maori or German telling them the date or time.
The first port is for English, second is Maori and third is German.

Running the transfer:
------------------------------------------------------------------------------------------------------------------------
1.) myserver program takes 3 unused ports as arguments from the command line. (Between 8000 and 64000)
Run on command line 
- python myserver.py 8000 8001 8002
In this case 8000 will be for English, 8001 will be for Maori and 8002 will be for German

2.) myclient program takes 3 arguments. Firstly either "date" or "time", second a host ip e.g "127.0.0.1" and lastly one of the unused ports specified with the server.
Examples of possible commands below.
Run on command line
- python myclient.py date 127.0.0.1 8000
- python myclient.py time 127.0.0.1 8001
- python myclient.py date 127.0.0.0 8002

Important:
------------------------------------------------------------------------------------------------------------------------
(Make sure to run myserver and myclient on two different command lines)
