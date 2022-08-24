import socket 
import sys

DATE, IP, PORTSTR = sys.argv[1:]

if (DATE != 'date') and (DATE != 'time'):
    print("Invalid parameter, specify date or time please")
    exit()
try:
    HOST = socket.gethostbyname(IP)
except:
    print("Host does not exist or IP address not in dotted notation")
    exit()
    
PORT = int(PORTSTR)
if (PORT < 1024) or (PORT > 64000):
    print("Invalid port number")
    exit()
    
ADDR = (HOST, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def packet_setup():
    packet = bytearray(6)
    MagicNo = 0x497E
    PacketType = 0x0001    
    if DATE == 'date':
        RequestType = 0x0001
    else:
        RequestType = 0x0002
    packet[0] = (MagicNo >> 8)
    packet[1] = (MagicNo & 0xff)
    packet[2] = (PacketType >> 8)
    packet[3] = (PacketType & 0xff)
    packet[4] = (RequestType >> 8)
    packet[5] = (RequestType & 0xff)   
    return packet

def check_msg(msg):
    if ((msg[0] << 8) + msg[1]) != 0x497E:
        print("Invalid MagicNo")
        exit()
    if ((msg[2] << 8) + msg[3]) != 0x0002:
        print("Invalid PacketType")
        exit()        
    if ((msg[4] << 8) + msg[5]) not in [0x0001, 0x0002, 0x0003]:
        print("Invalid language code")
        exit()       
    if ((msg[6] << 8) + msg[7]) > 2100:
        print("Invalid year")
        exit()        
    if (msg[8] < 1) or (msg[8] > 12):
        print("Invalid month")
        exit()        
    if (msg[9] < 1) or (msg[9] > 31):
        print("Invalid day")
        exit()        
    if (msg[10] < 0) or (msg[10] > 24):
        print("Invalid hour")
        exit()        
    if (msg[11] < 0) or (msg[11] > 59):
        print("Invalid minute")
        exit()        
    print_response(msg)

def print_response(msg):
    payload = msg[12:]
    MagicNo = (msg[0] << 8) + msg[1]
    PacketType = (msg[2] << 8) + msg[3]
    LanguageCode = (msg[4] << 8) + msg[5]
    Year = (msg[6] << 8) + msg[7]
    Month = msg[8]
    Day = msg[9]
    Hour = msg[10]
    Minute = msg[11]
    Length = msg[12]
    final = payload.decode()
    print(f"MagicNo = {hex(MagicNo)}")
    print(f"PacketType = {hex(PacketType)}")
    print(f"LanguageCode = {hex(LanguageCode)}")
    print(f"Year = {Year}")
    print(f"Month = {Month}")
    print(f"Day = {Day}")
    print(f"Hour = {Hour}")
    print(f"Minute = {Minute}")    
    print(f"Length = {Length}")  
    print(final[1:])    

client.sendto(packet_setup(), (IP, PORT))
client.settimeout(1)
try:
    msg = client.recv(1024)
except socket.timeout:
    print("Server did not respond within 1 second")
    exit()
check_msg(msg)
