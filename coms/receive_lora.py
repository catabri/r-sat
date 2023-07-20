import serial
import time
import codecs
from PIL import Image

serial_port = "/dev/ttyUSB0"
baud_rate = 9600

#Radio set up
freq = 915
mod = "SF9"
band_width = 125
tx_pr = 8
rx_pr = 8
power = 22

#RF configuration string
rf_conf_str = "AT+TEST=RFCFG,{},{},{},{},{},{},OFF,OFF,OFF\n".format(freq, mod, band_width>

#Serial Objet
ser = serial.Serial(serial_port,baud_rate)


def initialize_radio(): #Test PASSED
    ser.write("AT+MODE=TEST\n".encode())
    time.sleep(0.5)
    print(ser.readline().decode())
    time.sleep(0.5)
    ser.write(rf_conf_str.encode())
    print(ser.readline().decode())

def receive_msg():
    ser.write("AT+TEST=RXLRPKT".encode())
    while True:
        if ser.inWaiting():
            rx_msg = ser.readline().decode()
            if '+TEST: RX' in rx_msg:
               msg_data = rx_msg.split('\"')[-1]
            print(msg_data)

                                                                  
def chr_to_hex(string):
    return codecs.encode(string.encode(),'hex').decode()

def hex_to_chr(string):
    return codecs.decode(string, 'hex').decode()

initialize_radio()
time.sleep(1)

receive_msg()
