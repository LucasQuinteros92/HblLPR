
import sys
import os
import serial
import threading
import time
from modulos import auxiliar as auxiliar

from time import sleep 
from serial import SerialException

from modulos import hbl as hbl 
from modulos import log as log
from modulos.encoderWiegand import Encoder
from modulos import hblCore as hblCore
from modulos import variablesGlobales as variablesGlobales

global pi
 
STOPSERIAL = True
""" --------------------------------------------------------------------------------------------

    Thread para la comunicacion serial

-------------------------------------------------------------------------------------------- """

class LPR:
    def __init__(self, dataSerial, decodedData, Patente):
        self.dataSerial = dataSerial
        self.decodedData = decodedData
        self.Patente = Patente

        """Lee el puerto serie y extrea la patente del mensaje que envia el LPR
        """
def stop():
    global STOPSERIAL
    STOPSERIAL = False
    
def startThreadSerial(): 

    global pi

    ser = serial.Serial(port=hbl.SERIAL_port, 
                        baudrate=hbl.SERIAL_baudrate, 
                        bytesize=hbl.SERIAL_bytesize, 
                        parity=hbl.SERIAL_parity, 
                        stopbits=hbl.SERIAL_stopbits, 
                        timeout=0.1)
    ser.flushInput()
    
    cLPR = LPR("","","")
              
    while STOPSERIAL: 

        if hbl.FUNC_modo == 8:

            try: 
                
                cLPR.dataSerial = ser.readline()
                #cLPR.dataSerial = str(input("Ingrese patente"))
                #time.sleep(0.03)
 
                #data_left = ser.inWaiting()
                #received_data +=ser.read(data_left) 

                if len(cLPR.dataSerial) > 0:

                    log.escribeSeparador(hbl.LOGS_hblSerial)
                    try:
                        """Decodifico el msg"""
                        cLPR.decodedData = cLPR.dataSerial.decode('utf-8', errors='ignore')
                        """Elimino el ultimo caracter porque la camara me agrega una U al final"""
                        cLPR.Patente = cLPR.decodedData[:-1]
                        cLPR.Patente=cLPR.Patente.replace("\x00","")
                    except Exception as e:
                        print("Error en la lectura de patente")
                        cLPR.Patente = str(cLPR.dataSerial)
                    log.escribeLineaLog(hbl.LOGS_hblSerial, "PATENTE : " + str(cLPR.Patente)) 
                    
                    #La siguiente linea borra el primer elemento de la lista y lo agrega al final para luego ser pisado en la siguiente linea
                    try:
                        variablesGlobales.listaPatentes.append(variablesGlobales.listaPatentes.pop(0))
                        variablesGlobales.listaPatentes[len(variablesGlobales.listaPatentes)-1] = str(cLPR.Patente)
                        log.escribeLineaLog(hbl.LOGS_hblSerial,str(variablesGlobales.listaPatentes))
                    except Exception as e:
                        print("Error al agregar patente a la lista")
    
            except Exception as e:
              
                exc_type, exc_obj, exc_tb = sys.exc_info() 
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
                errorExcepcion = "ERROR : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

                log.escribeSeparador(hbl.LOGS_hblSerial)
                log.escribeLineaLog(hbl.LOGS_hblSerial, "Error : " + str(errorExcepcion)) 
        
        time.sleep(0.01)
    
""" --------------------------------------------------------------------------------------------

    inicializacion comunicacion Serial

-------------------------------------------------------------------------------------------- """

def inicializacion(pi2): 

    global pi
 
    pi = pi2
    
    

    if hbl.SERIAL_activado == 1:
 
        try:

            serialHBL = threading.Thread(target=startThreadSerial, name='HBLSerial')
            serialHBL.setDaemon(True)
            serialHBL.start()   

            log.escribeSeparador(hbl.LOGS_hblSerial)
            log.escribeLineaLog(hbl.LOGS_hblSerial, "Serial Start")  
        
        except Exception as e:
              
            exc_type, exc_obj, exc_tb = sys.exc_info() 
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
            errorExcepcion = "ERROR : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

            log.escribeSeparador(hbl.LOGS_hblSerial)
            log.escribeLineaLog(hbl.LOGS_hblSerial, "Error : " + str(errorExcepcion))         