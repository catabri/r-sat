import board
import busio
import adafruit_gps
import serial
import sys
import datetime
import pandas as pd
import time

uart = None
gps  = None
_, n_msr, interval_time = sys.argv
n_msr = int(n_msr)
interval_time = float(interval_time)
now = datetime.datetime.now()
name = now.strftime("%m-%d-%H-%M-%S")
logfile = f"/home/pi/log/log{name}.txt"


def escribir(ruta_archivo, nueva_fila):
    # Leer el archivo CSV existente)
    df = pd.DataFrame(nueva_fila)
    df = df.T
    # Guardar el DataFrame actualizado en el archivo CSV
    df.to_csv(ruta_archivo,mode="a",header =False, index=False)

def main():
    i = 0
    uart = serial.Serial("/dev/serial0", baudrate=115200, timeout=10)
    gps = adafruit_gps.GPS(uart)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    gps.send_command(b"PMTK220,1000")
    with open(logfile, "w") as filex:
        while i<n_msr:
            time.sleep(interval_time)
            try:
                print('estoy intentando ;-;')
                data = gps.read(185)  # read up to 32 bytes
                if data is not None:
                    data_string = "".join([chr(b) for b in data])
                    filex.write(data_string)
                    print(data_string, end="")
                    #print(' what tha heeeeellll')
                    i+=1
                    escribir("mensaje.csv",data_string)
            except Exception:
                print("Failed reading data... trying again")
                escribir("mensaje.csv",['P','E','P','E','G','A','Y','P','E','P','E','G','A','Y','P','E','P','E','G','A','Y','P','E','P','E','G','A','Y','P','E','P','E','G','A','Y','P','E','P','E','G','A','Y','P','E','P','E','G','A','Y','!'])
            except KeyboardInterrupt:
                print("Nos vimos!")
                exit(0)




if __name__ == "__main__":
    escribir("mensaje.csv",['P','E','P','E','G','A','Y','P','E','P','E','G','A','Y','P','E','P','E','G','A','Y','P','E','P','E','G','A','Y','P','E','P','E','G','A','Y','P','E','P','E','G','A','Y','P','E','P','E','G','A','Y','!'])
    main()
