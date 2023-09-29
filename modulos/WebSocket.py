import websocket
import time

import requests
import ssl
import json
from threading import Thread 
from modulos import hbl as hbl
from modulos import log as log
from modulos import variablesGlobales as vg
from modulos import dobleFactor_LPR_DNI as dbFactor

"""
    *Para usar la libreria de websocket, hay que instalar:
        pip3 install websocket-client
        pip3 install rel
    Si se comete el error de instalar el paquete de websocket, hacer lo siguiente:
        pip3 uninstall websocket
        pip3 uninstall websocket-client
        pip3 install websocket-client

    *Hay dos tipos de eventos:
        # IDENTIFY_SUCCESS_FINGERPRINT
        # VERIFY_SUCCESS_CARD
"""  
class WebSocket(object):
    
    def __init__(self) :
        if hbl.WebSocket_activado:
            #websocket.enableTrace(True)
            self.connected = False
            self.reconnected = False
            self.reRun = True
            #self.SALUDO = json.dumps({
            #    "conexionCliente": hbl.HblID
            #})
            #self.SALUDO = json.dumps(
            #
            #    {"evento":"nuevoingreso", 
            #     "datos":{
            #        "Persona": "3185254", 
            #        "Vehiculo": "AA123AA",
            #        "fechaHora": 1686767849000,
            #        "clientId": "100000002",
            #        "clientName":"HBL2"},
            #     "msjID":"1686767849"}
            #
            #)
            self.connect()
    def connect(self):
        try:
            self.ws = websocket.WebSocketApp(hbl.WebSocket_WebSocket_Host,
                                                on_open=self.on_open,
                                                on_message=self.on_message,
                                                on_error=self.on_error,
                                                on_close=self.on_close,
                                                header = {hbl.WebSocket_Header},
                                                cookie= '{"Token": "'+hbl.WebSocket_Token+'","ClientId": "'+hbl.WebSocket_ClientId+'"} ' )
            #self.ws.on_message = dbFactor.Validacion_Doble_Factor.nuevoEventoRecibido
            self.connected = False
            self.reRun = True
            self.t = Thread( target=self.__run, daemon=False,name ="Websocket")
            self.t.start()
        except Exception as e:
            print(str(e))
            log.escribeLineaLog(hbl.LOGS_WebSocket,"Conexion no establecida")

    def __run(self):
        try:
            self.ws.run_forever(reconnect= 2, 
                                ping_interval= 5,
                                ping_timeout= 3,
                                sslopt={"cert_reqs": ssl.CERT_NONE})  
            # Set dispatcher to automatic reconnection,
            # 5 second reconnect delay if connection closed unexpectedly
            
            #sslopt={"cert_reqs": ssl.CERT_NONE}
        except:
            pass
        
    def on_open(self,ws):
        self.connected = True
        self.reconnected = True
        self.__LogReport("Conexion establecida")
        #self.send_message(self.SALUDO)
        
    def on_message(self, ws, message):
        self.__LogReport("Mensaje Entrante: "+ str(message))
        #{"id" : "24997319-0" , "dominio" : ""}
    
    def on_error(self,ws, error):
        self.connected = False 
        self.__LogReport("OnError: "+ str(error))
        self.__LogReport("Reiniciando conexion")
        self.ws.ping_timeout = 3
        self.ws.ping_interval = 5
        #if str(error) == "ping/pong timed out" or str(error) == "[Errno 113] No route to host":
        time.sleep(2)
        
        self.ws.close()
        if self.reRun:
            self.connect()
            
        #log.escribeLineaLog(hbl.LOGS_hblBioStar2_WebSocket,"Error : " + str(error))
    
    

    def on_close(self,ws, close_status_code, close_msg):
        self.connected = False
        self.ws.close()
        self.__LogReport("Conexion Terminada\n"+"close msg: " + str(close_msg) + 
                        "\ncode: "+ str(close_status_code))
        if self.reRun:
            self.connect()

    def stop(self):
        self.reRun = False
        self.ws.close()
        self.__LogReport("Websocket STOPED")

    def on_data(self,arg1,arg2,arg3):
        print("### New Data ###")
        
    def send_message(self, mensaje):
        res = False
        try:
            self.ws.send(mensaje)
            self.__LogReport("Mensaje Enviado: "+ str(mensaje))
            res = True
        except Exception as e:
            self.__LogReport("Error al enviar mensaje: "+ str(mensaje)+"\n Error:"+str(e))
            res = False
            
        return res

    def estaConectado(self):
        return self.connected 

    def __LogReport(self, mensaje):
        log.escribeSeparador(hbl.LOGS_WebSocket)
        log.escribeLineaLog(hbl.LOGS_WebSocket, mensaje)