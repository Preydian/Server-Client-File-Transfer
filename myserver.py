# coding: utf8
import socket 
from datetime import date
from datetime import datetime 
import sys
import select

ENGLISH = ['filler' , 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']         
GERMAN = ['filler', 'Januar', 'Februar', 'Marz', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
MAORI = ['filler', 'Hui-tanguru', 'Poutu-te-rangi', 'Paenga-whawha', 'Haratua', 'Pipiri', 'Hongongoi', 'Here-turi-koka', 'Mahuru', 'Whiringa-a-nuku', 'Whiringa-a-rangi', 'Hakihea'] 
HOST = '0.0.0.0'
try:
    PORT1, PORT2, PORT3 = sys.argv[1:]
except:
    print("Too many inputs")
ADDRENG = (HOST, int(PORT1))
ADDRMAR = (HOST, int(PORT2))
ADDRGER = (HOST, int(PORT3))

def verify_ports():    
    if (len(set([PORT1,PORT2,PORT3])) != 3):
        print("Not all ports are unique")
        exit()        
    if (int(PORT1) < 1024) or (int(PORT1) > 64000):
        print("Port one outside range 1024 - 64000")
        exit()
    if (int(PORT2) < 1024) or (int(PORT2) > 64000):
        print("Port two outside range 1024 - 64000")
        exit()
    if (int(PORT3) < 1024) or (int(PORT3) > 64000):
        print("Port three outside range 1024 - 64000")    
        exit()
def set_up_binding():
    print("Binding's ready")
    try:
        serverENG = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverMAR = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverGER = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverENG.bind(ADDRENG)
        serverMAR.bind(ADDRMAR)
        serverGER.bind(ADDRGER)
    except:
        print("Failed to bind ports")
        exit()
    return serverENG, serverMAR, serverGER
      
def handle_client(serverENG, serverMAR, serverGER):
    while True:
        print(f"New connection established.")
        socket_list = [serverENG, serverMAR, serverGER]
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        for sock in read_sockets:
            if sock == serverENG:
                hold, sourceAddress = serverENG.recvfrom(1024)
                verify_packet(hold)              
                serverENG.sendto(DT_response(hold, "Eng"), sourceAddress)
            elif sock == serverMAR:
                hold, sourceAddress = serverMAR.recvfrom(1024)
                verify_packet(hold)
                serverMAR.sendto(DT_response(hold, "Mar"), sourceAddress)
            elif sock == serverGER:
                hold, sourceAddress = serverGER.recvfrom(1024)
                verify_packet(hold)
                serverGER.sendto(DT_response(hold, "Ger"), sourceAddress) 
                
def verify_packet(packet):
    if len(packet) != 6:
        print("Invalid packet size")
        exit()
    if ((packet[0] << 8) + packet[1]) != 0x497E:
        print("Invalid MagicNo")
        exit()
    if ((packet[2] << 8) + packet[3]) != 0x0001:
        print("Invalid PacketType")
        exit()
    if ((packet[4] << 8) + packet[5]) != 0x0001 and ((packet[4] << 8) + packet[5]) != 0x0002:
        print("Invalid RequestType")
        exit()

def get_date_and_time():
    today = date.today()
    value = today.strftime("%d/%m/%Y")
    day = int(value[0:2])
    month = int(value[3:5])
    year = int(value[6:])    
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    hour = int(time[0:2])    
    minute = int(time[3:5]) 
    return (year, month, day, hour, minute)

def create_payload(packet, language, year, month, day, hour, minute):
    if language == 'Eng':
        language_code = 0x0001
        if ((packet[4] << 8) + packet[5]) == 0x0001:
            payload = f'Today’s date is {ENGLISH[month]} {day}, {year}'
        else:
            payload = f'The current time is {hour}:{minute}'
    elif language == 'Mar':
        language_code = 0x0002
        if ((packet[4] << 8) + packet[5]) == 0x0001:
            payload = f'Ko te ra o tenei ra ko {MAORI[month]} {day}, {year}'
        else:
            payload = f'Ko te wa o tenei wa {hour}:{minute}'        
    elif language == 'Ger':
        language_code = 0x0003
        if ((packet[4] << 8) + packet[5]) == 0x0001:
            payload = f'Heute ist der {GERMAN[month]} {day}, {year}'
        else:
            payload = f'Die Uhrzeit ist {hour}:{minute}'     
    payload_bytes = payload.encode('utf-8')
    if len(payload_bytes) > 255:
        print("T is too long")
        exit()
    return payload, payload_bytes, language_code

def DT_response(packet, language):
    RequestType = 0x0002    
    year, month, day, hour, minute = get_date_and_time()
    payload, payload_bytes, language_code = create_payload(packet, language, year, month, day, hour, minute)
    response_packet = bytearray(13 + len(payload_bytes))
    response_packet[0] = packet[0]
    response_packet[1] = packet[1]
    response_packet[2] = RequestType >> 8
    response_packet[3] = RequestType & 0xff
    response_packet[4] = language_code >> 8
    response_packet[5] = language_code & 0xff
    response_packet[6] = year >> 8
    response_packet[7] = year & 0xff
    response_packet[8] = month
    response_packet[9] = day
    response_packet[10] = hour
    response_packet[11] = minute
    response_packet[12] = len(payload)
    index = 13
    for byte in payload_bytes:
        response_packet[index] = byte
        index += 1
    return response_packet  

def start():
    verify_ports()
    eng, mar, ger = set_up_binding()
    handle_client(eng, mar, ger)

print("SERVER IS STARTING...")
start()