import glob,time,msvcrt,operator
from multiprocessing import Condition
from collections import Counter
import os
import time

def dife_fecha():
    mes= time.strftime("%m")    
    if mes == '01':
        mes = 'ENERO'
    if mes == '02':
        mes = 'FEBRERO'
    if mes == '03':
        mes = 'MARZO'
    if mes == '04':
        mes = 'ABRIL'
    if mes == '05':
        mes = 'MAYO'
    if mes == '06':
        mes = 'JUNIO'
    if mes == '07':
        mes = 'JULIO'
    if mes == '08':
        mes = 'AGOSTO'
    if mes == '09':
        mes = 'SEPTIEMBRE'
    if mes == '10':
        mes = 'OCTUBRE'
    if mes == '11':
        mes = 'NOVIEMBRE'
    if mes == '12':
        mes = 'DICIEMBRE'
    return mes

condicion = 1

while condicion == 1:

    ubicacion = int(input("\n1.Dia\n2.Ubicacion Personalizada\n3.Hoy\nIngrese: "))

    if ubicacion == 1:
        ano= input("Ingrese año: ")
        mes= input("Ingrese mes: ")
        dia= input("Ingrese dia: ")
        ruta = "\\\TRUENAS\\RedjudicialN1\\Redjudicial_estados\\"+ano+"\\"+mes+"\\"+dia+"\\"

    elif ubicacion == 2:
        ruta = input("Ingrese la ruta: ")

    elif ubicacion == 3:
        mes = dife_fecha()
        dia = time.strftime("%d") 
        ano = time.strftime("%Y")
        ruta = "\\\TRUENAS\\RedjudicialN1\\Redjudicial_estados\\"+ano+"\\"+mes+"\\"+dia+"\\"
        
    total=0
    departamentos = []


    print("----------------------\nESTADOS\n----------------------")

    ext = ["PNG","JPG","TXT","DB","MP4"]
    ciudades = ["CARTAGO","BUENAVENTURA","TULUA","BUGA","POPAYAN"]
    for archivo in glob.glob(ruta+"\\**", recursive=True):
        archivo = archivo.upper()
        if ("." in archivo) and ("YA." not in archivo) and (archivo.split(".")[-1] not in ext ):
            print(archivo[49:])
            total+=1


    print("\n----------------------\nTOTAL:",total,"\n----------------------")
    condicion =int(input("\n1.Reiniciar\n2.Cerrar\nIngrese: "))
    os.system ("cls")


print("\nPULSE UNA TECLA PARA CERRAR...")
msvcrt.getch()
