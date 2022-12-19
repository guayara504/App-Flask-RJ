
from flask import Flask, render_template, request,redirect,url_for
import database as db


import glob,time,msvcrt,operator
from multiprocessing import Condition
from collections import Counter
import os
import time


app =  Flask(__name__)

@app.route('/')
def index():
    cursor = db.database.cursor()
    cursor.execute("""SELECT z01_radicacion_juzgado,ciudad,fecha_ingreso,digitador
                FROM z04_estado  
                WHERE fecha_notificacion LIKE "%2022%"
                GROUP BY z01_radicacion_juzgado,ciudad
                ORDER BY fecha_notificacion DESC""")
    result1 = cursor.fetchall()
    data1= []
    columnNames = [column[0] for column in cursor.description ]
    for record in result1[:5]:
        data1.append(dict(zip(columnNames,record)))


    cursor.execute("""SELECT z01_radicacion_juzgado,z01_radicacion_z01_radicacion,demandante,demandado,ciudad,fecha_ingreso,digitador
FROM z04_estado
WHERE
		#FECHA A REVISAR
		(fecha_notificacion LIKE "%2022%"
		#fecha_notificacion = CURDATE()
		
		#REVISAR ESPACIOS EN JUZGADOS Y CIUDADES AL PRINCIPIO Y AL FINAL
		AND ((z01_radicacion_juzgado LIKE " %" OR ciudad LIKE " %" OR z01_radicacion_juzgado LIKE "% " OR ciudad LIKE "% ")
		
		#REVISAR RADICACIONES FUERA DEL RANGO DE DIGITACION Y QUE NO TERMINEN EN 0001
		OR ((z01_radicacion_z01_radicacion NOT BETWEEN "195000000" AND "202299999") AND z01_radicacion_z01_radicacion NOT LIKE ("%0001") AND z01_radicacion_z01_radicacion NOT LIKE ("%660884089%") AND z01_radicacion_z01_radicacion NOT LIKE ("%768924001%"))
		
		#REVISAR JUZGADOS SIN NUMERO 
		OR (z01_radicacion_juzgado NOT LIKE "%0"
		AND z01_radicacion_juzgado NOT LIKE "%1"
		AND z01_radicacion_juzgado NOT LIKE "%2"
		AND z01_radicacion_juzgado NOT LIKE "%3"
		AND z01_radicacion_juzgado NOT LIKE "%4"
		AND z01_radicacion_juzgado NOT LIKE "%5"
		AND z01_radicacion_juzgado NOT LIKE "%6"
		AND z01_radicacion_juzgado NOT LIKE "%7"
		AND z01_radicacion_juzgado NOT LIKE "%8"
		AND z01_radicacion_juzgado NOT LIKE "%9"
		AND z01_radicacion_juzgado NOT LIKE "CONSEJO%"
		AND z01_radicacion_juzgado NOT LIKE "CORTE%"
		AND z01_radicacion_juzgado NOT LIKE "TRIBUNAL%")
		
		#REVISAR JUZGADOS CON EL NUMERO SIN ESPACIO
		OR  (z01_radicacion_juzgado NOT LIKE "% 0%"
		AND z01_radicacion_juzgado NOT LIKE "% 1%"
		AND z01_radicacion_juzgado NOT LIKE "% 2%"
		AND z01_radicacion_juzgado NOT LIKE "% 3%"
		AND z01_radicacion_juzgado NOT LIKE "% 4%"
		AND z01_radicacion_juzgado NOT LIKE "% 5%"
		AND z01_radicacion_juzgado NOT LIKE "% 6%"
		AND z01_radicacion_juzgado NOT LIKE "% 7%"
		AND z01_radicacion_juzgado NOT LIKE "% 8%"
		AND z01_radicacion_juzgado NOT LIKE "% 9%"
		AND z01_radicacion_juzgado NOT LIKE "CONSEJO%"
		AND z01_radicacion_juzgado NOT LIKE "CORTE%"
		AND z01_radicacion_juzgado NOT LIKE "TRIBUNAL%")
		
		#REVISAR JUZGADOS CON CARACTERES DIFERENTES AL INICIO
		OR (z01_radicacion_juzgado NOT LIKE "J%"
		AND z01_radicacion_juzgado NOT LIKE "T%"
		AND z01_radicacion_juzgado NOT LIKE "C%")
		
		#REVISAR JUZGADOS CON DOBLE ESPACIO ANTES DEL NUMERO
		OR (z01_radicacion_juzgado  LIKE "%  %")
		
		#DOBLE "DE" EN EL JUZGADO
		OR (z01_radicacion_juzgado LIKE "%DE DE%"
		AND z01_radicacion_juzgado NOT LIKE "%DESC%")
		
		#Revisar Linea con doble linea
		OR (z01_radicacion_juzgado LIKE "%\n%" 
			 OR z01_radicacion_z01_radicacion LIKE "%\n%" 
			 OR ciudad LIKE "%\n%"
			 OR demandante LIKE "%\n%" 
			 OR demandado LIKE "%\n%" 
			 OR clase_proceso LIKE "%\n%")
		
		OR (clase_proceso = " " OR demandante = " " OR demandado = " "
			 OR clase_proceso = "  " OR demandante = "  " OR demandado = "  ")
		OR (z01_radicacion_z01_radicacion LIKE "%____00000%"))
		)
		#Revisar Fecha Notificacion Mala
		OR fecha_notificacion LIKE "0000-00-00" """)
    result2 = cursor.fetchall()
    data2= []
    columnNames = [column[0] for column in cursor.description ]
    for record in result2:
        data2.append(dict(zip(columnNames,record)))
 
    cursor.close()

    return render_template('index.html',data1=data1,data2=data2)

@app.route("/revisar")
def rev():
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


    mes = dife_fecha()
    dia = time.strftime("%d") 
    ano = time.strftime("%Y")
    ruta = "\\\TRUENAS\\RedjudicialN1\\Redjudicial_estados\\"+ano+"\\"+mes+"\\"+dia+"\\"
        
    total=0
    departamentos = []


    print("----------------------\nESTADOS\n----------------------")
    archivos = []
    ext = ["PNG","JPG","TXT","DB","MP4"]
    ciudades = ["CARTAGO","BUENAVENTURA","TULUA","BUGA","POPAYAN"]
    for archivo in glob.glob(ruta+"\\**", recursive=True):
        archivo = archivo.upper()
        if ("." in archivo) and ("YA." not in archivo) and (archivo.split(".")[-1] not in ext ):
            print(archivo[49:])
            total+=1
            archivos.append(archivo[49:])


    print("\n----------------------\nTOTAL:",total,"\n----------------------")
    return render_template('pdf.html',data=archivos) 

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
