import threading
import os
import sys
import pigpio
import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs
import signal

import datetime 
import json
from modulos import hbl as hbl
from modulos import delays as delays
from modulos import log as log
from modulos import i2cDevice as i2cDevice
from modulos import variablesGlobales as VG


global pi

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def getOldDatafromFile(self):
        VG.mutexBBDD_DNI_Patente.acquire()
        with open('/usr/programas/hbl/modulos/BBDD_RUT_Patente.json') as f:
            oldData = json.load(f)
            #print("oldData" + str(oldData))
        VG.mutexBBDD_DNI_Patente.release()
        return oldData
    
    def updateDatainFile(self,newData):
        VG.mutexBBDD_DNI_Patente.acquire()
        with open('/usr/programas/hbl/modulos/BBDD_RUT_Patente.json', 'w') as convert_file:
            convert_file.write(json.dumps(newData,indent=6))
        VG.mutexBBDD_DNI_Patente.release()
            
    def addDatainFile(self):
        try:
            if str(self.plate) == "":
                errorStr = "Patente invalida"
                log.escribeLineaLog(hbl.LOGS_hblHTTP, errorStr)
                return errorStr
            oldData = self.getOldDatafromFile()
            patentes = oldData.get(str(self.id))
            if patentes is None:
                log.escribeLineaLog(hbl.LOGS_hblHTTP, "Nuevo ID")
                oldData[str(self.id)] = [str(self.plate)]
            else:
                log.escribeLineaLog(hbl.LOGS_hblHTTP, "ID ya existe")
                """Check si la patente no esta ya"""
                if str(self.plate) in patentes:
                    errorStr = "Patente ya existe"
                    log.escribeLineaLog(hbl.LOGS_hblHTTP, errorStr)
                    return errorStr
                else:
                    oldData[str(self.id)].append(str(self.plate))
                
            #print("newData" + str(oldData))
            self.updateDatainFile(oldData)
            VG.newDataBBDD = True
            log.escribeLineaLog(hbl.LOGS_hblHTTP, "BBDD actualizada")
            return oldData
        except Exception as e:
            log.escribeLineaLog(hbl.LOGS_hblHTTP, "Error al agregar data: " + str(e))
        
    
    def removeDatainFile(self):
        try:
            oldData = self.getOldDatafromFile()
            if oldData.get(str(self.id)) is None:
                errorStr = "El ID no existe"
                log.escribeLineaLog(hbl.LOGS_hblHTTP, errorStr)
                return errorStr
            else:
                print("oldData" + str(oldData))
                if self.plate == "": # si no se especifica la patente, se borran todas
                    oldData.pop(str(self.id))
                else:
                    if str(self.plate) in oldData.get(str(self.id)): #Me fijo si la patente existe
                        oldData[str(self.id)].remove(str(self.plate)) #Borro la patente      
                    else:
                        errorStr = "La patente no existe"
                        log.escribeLineaLog(hbl.LOGS_hblHTTP, errorStr)
                        return errorStr                 
                print("newData" + str(oldData))
                self.updateDatainFile(oldData)
                VG.newDataBBDD = True
                log.escribeLineaLog(hbl.LOGS_hblHTTP, "BBDD actualizada")
            
            return oldData
        except Exception as e:
            log.escribeLineaLog(hbl.LOGS_hblHTTP, "Error al agregar data: " + str(e))
        
        
    def do_GET(self): 

        self.id = 0
        self.tiempo = 0
        self.linea1 = ""
        self.linea2 = ""
        self.linea3 = ""
        self.linea4 = ""
        self.action = ""
        self.idWD = ""
        self.plate = ""

        # ex : http://172.16.1.157:8000/?id=1&tiempo=1000

        # envia la respuesta '200 OK'  
        self.send_response(200)

        # setea el header de la pagina
        self.send_header("Content-type", "text/html")

        # Whenever using 'send_header', you also have to call 'end_headers'
        self.end_headers()

        # extrae el parametro del query 
        query_components = parse_qs(urlparse(self.path).query)

        if 'id' in query_components:
            self.id = query_components["id"][0]
             
        if 'tiempo' in query_components:
            self.tiempo = query_components["tiempo"][0] 

        if 'linea1' in query_components:
            self.linea1 = query_components["linea1"][0]
            i2cDevice.lcd1.put_line(0, self.linea1) 

        if 'linea2' in query_components:
            self.linea2 = query_components["linea2"][0]
            i2cDevice.lcd1.put_line(1, self.linea2) 

        if 'linea3' in query_components:
            self.linea3 = query_components["linea3"][0]
            i2cDevice.lcd1.put_line(2, self.linea3) 

        if 'linea4' in query_components:
            self.linea4 = query_components["linea4"][0]
            i2cDevice.lcd1.put_line(3, self.linea4)
        
        if 'action' in query_components:
            self.action = query_components["action"][0]
        
        if 'plate' in query_components:
            self.plate = query_components["plate"][0]
            
            
 
         

        # activa salidas segun tiempo indicado 
        if id == "1":   
            pi.write(hbl.DIG_out_pin_out1, hbl.ON)  
            delays.ms(int(self.tiempo))
            pi.write(hbl.DIG_out_pin_out1, hbl.OFF)  
        elif id == "2": 
            pi.write(hbl.DIG_out_pin_out2, hbl.ON)     
            delays.ms(int(self.tiempo))
            pi.write(hbl.DIG_out_pin_out2, hbl.OFF)  
        elif id == "3": 
            pi.write(hbl.DIG_out_pin_out3, hbl.ON)     
            delays.ms(int(self.tiempo))
            pi.write(hbl.DIG_out_pin_out3, hbl.OFF) 
        elif id == "4": 
            pi.write(hbl.DIG_out_pin_out4, hbl.ON)     
            delays.ms(int(self.tiempo))
            pi.write(hbl.DIG_out_pin_out4, hbl.OFF) 
        elif id == "5": 
            pi.write(hbl.DIG_out_pin_out5, hbl.ON)     
            delays.ms(int(self.tiempo))
            pi.write(hbl.DIG_out_pin_out5, hbl.OFF)
        elif id == "6": 
            pi.write(hbl.DIG_out_pin_out6, hbl.ON)     
            delays.ms(int(self.tiempo))
            pi.write(hbl.DIG_out_pin_out6, hbl.OFF) 
        elif id == "7": 
            pi.write(hbl.DIG_out_pin_out7, hbl.ON)     
            delays.ms(int(self.tiempo))
            pi.write(hbl.DIG_out_pin_out7, hbl.OFF) 
        elif id == "8": 
            pi.write(hbl.DIG_out_pin_out8, hbl.ON)     
            delays.ms(int(self.tiempo)) 
            pi.write(hbl.DIG_out_pin_out8, hbl.OFF)  
        else:
            pass

        log.escribeSeparador(hbl.LOGS_hblHTTP) 
        if id != 0:
            # escribe en el log
            log.escribeLineaLog(hbl.LOGS_hblHTTP, "action  : " + str(self.action))
            log.escribeLineaLog(hbl.LOGS_hblHTTP, "ID  : " + str(self.id))
            log.escribeLineaLog(hbl.LOGS_hblHTTP, "plate : " + str(self.plate))
        if str(self.action) == "add":
            newBBDD = self.addDatainFile()
        if str(self.action) == "remove":
            newBBDD = self.removeDatainFile()
                
            
        if hbl.HTTP_server_respuesta == 1:
            html = json.dumps(newBBDD,indent=6)
            print(str(self.action) + str(self.idWD) + str(self.plate))
            # escribe el contenido html con UTF-8
            self.wfile.write(bytes(html, "utf8")) 
            

        return

""" --------------------------------------------------------------------------------------------

 


-------------------------------------------------------------------------------------------- """ 

def startServer():

    try:

        # Create an object of the above class
        handler_object = MyHttpRequestHandler

        my_server = socketserver.TCPServer(("", hbl.HTTP_server_port), handler_object)
        
        # Star the server
        my_server.serve_forever()  
    
    except Exception as inst:

        log.escribeSeparador(hbl.LOGS_hblHTTP) 
        log.escribeLineaLog(hbl.LOGS_hblHTTP, "Error : " + str(inst)) 

        # sale del programa y hace un kill a los procesos activos de python
        os.system("sudo killall -v python3")

    while True:
        pass

""" --------------------------------------------------------------------------------------------

 


-------------------------------------------------------------------------------------------- """ 

def inicializacion(pi2): 

    global pi

    pi = pi2

    if hbl.HTTP_server_activado == 1:

        http = threading.Thread(target=startServer, name='ServerHTTP')
        http.setDaemon(True)
        http.start()

        log.escribeSeparador(hbl.LOGS_hblHTTP) 
        log.escribeLineaLog(hbl.LOGS_hblHTTP, "HTTP Server iniciado en el puerto : " + str(hbl.HTTP_server_port))