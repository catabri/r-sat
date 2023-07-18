import board
import busio
import adafruit_gps
import serial
import sys
import datetime
import pandas as pd
import time
import csv

uart = None
gps  = None
_, n_msr, interval_time = sys.argv
n_msr = int(n_msr)
interval_time = float(interval_time)
now = datetime.datetime.now()
name = now.strftime("%m-%d-%H-%M-%S")
logfile = f"/home/pi/log/log{name}.txt"

#Función que escribe la última linea en el csv  ruta_archivo
def escribir(ruta_archivo, nueva_fila):
    # Leer el archivo CSV existente)
    df = pd.DataFrame(nueva_fila)
    df = df.T
    # Guardar el DataFrame actualizado en el archivo CSV
    df.to_csv(ruta_archivo,mode="a",header =False, index=False)

#Procesa la data de gps para tener los datos importantes en una lista
def data_processing(data_string):
    list_data = data_string.split()
    GNGGA = list_data[3].split(',')
    GNRMC = list_data[4].split(',')
    data2 = GNGGA[9:11]
    data1 = GNRMC[1:8]
    for i in data2:
      data1.append(i)
    return data1

#Función que extrae la última linea de un csv
def line_csv(file_csv):
    with open(file_csv,'r') as archivo:
      read_csv = csv.reader(archivo)
      for line in read_csv:
           last_line =  line
      return last_line

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
                data = gps.read(185)
                if data is not None:
                    data_string = "".join([chr(b) for b in data])
                    print(data_string, end="")
                    
                    procesado = data_processing(data_string)
                    
                    thp = line_csv("../inst/rsatinstrumentation/sensores/temperatura/aht10/data_aht10.csv") #Esto desde la carpeta software en la raspberry
                    presion = line_csv("../inst/rsatinstrumentation/sensores/presion/data_bmp180.csv")[1] #Esto desde la carpeta software en la raspberry
                    thp.append(presion)
                    procesado+=thp
                    escribir("mensaje_principal.csv",procesado)
                    print('\nMensaje Escrito!!!')
                    i += 1
                    raise KeyboardInterrupt
            except Exception:
                print("Failed reading data... trying again")
                
            except KeyboardInterrupt:
                print("Nos vimos!")
                exit(0)



if __name__ == "__main__":
    main()
