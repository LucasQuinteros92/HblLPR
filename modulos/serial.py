
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

    #ser = serial.Serial(port=hbl.SERIAL_port, 
    #                    baudrate=hbl.SERIAL_baudrate, 
    #                    bytesize=hbl.SERIAL_bytesize, 
    #                    parity=hbl.SERIAL_parity, 
    #                    stopbits=hbl.SERIAL_stopbits, 
    #                    timeout=1)
    ser = serial.Serial(port=hbl.SERIAL_COM1_port, 
                         baudrate=hbl.SERIAL_COM1_baudrate, 
                         bytesize=hbl.SERIAL_COM1_bytesize, 
                         parity=hbl.SERIAL_COM1_parity, 
                         stopbits=hbl.SERIAL_COM1_stopbits,
                         timeout=hbl.SERIAL_COM1_timeout)
    ser.flushInput()
    
    cLPR = LPR("","","")
              
    while STOPSERIAL: 

            try: 
                
                cLPR.dataSerial = ser.readline()
                #cLPR.dataSerial = str(input("Ingrese patente"))
                #time.sleep(0.03)
 
                #data_left = ser.inWaiting()
                #received_data +=ser.read(data_left) 

                if len(cLPR.dataSerial) > 0:
                    #print(str(cLPR.dataSerial))
                    log.escribeSeparador(hbl.LOGS_hblSerial)
                    try:
                        """Decodifico el msg"""
                        cLPR.decodedData = cLPR.dataSerial.decode('utf-8', errors='ignore')
                        """Elimino el ultimo caracter porque la camara me agrega una U al final"""
                        cLPR.Patente = cLPR.decodedData[:-1]
                        cLPR.Patente=cLPR.Patente.replace("\x00","")
                        cLPR.Patente = cLPR.Patente.strip()
                        variablesGlobales.ultimaPatente = cLPR.Patente
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

    log.escribeSeparador(hbl.LOGS_hblSerial)
    log.escribeLineaLog(hbl.LOGS_hblSerial, "SERIAL1 STOPED") 

def startThreadSerial2(): 
    #auxiliar.EscribirFuncion("startThreadSerial2")
    #uso hblReporte para no generar un nuevo log en productivo, y que sea mas claro
    #cuando se recibe un wiegand via serial
    global pi
    global ser2

    ser2 = serial.Serial(port=hbl.SERIAL_COM2_port, 
                         baudrate=hbl.SERIAL_COM2_baudrate, 
                         bytesize=hbl.SERIAL_COM2_bytesize, 
                         parity=hbl.SERIAL_COM2_parity, 
                         stopbits=hbl.SERIAL_COM2_stopbits,
                         timeout=hbl.SERIAL_COM2_timeout)
    #ser2.write(b"Serial start")
    ser2.flushInput()
              
    while STOPSERIAL: 

        if hbl.SERIAL_COM2_activado == 1:
            

                try: 
                    Serial_COM2_Rx_Data = ser2.readline()
                    #time.sleep(0.03)
                    #data_left = ser2.inWaiting()
                    #VG.Serial_COM2_Rx_Data +=ser2.read(data_left) 
                    if(len(Serial_COM2_Rx_Data) > 0):
                        #Serial_COM2_Rx_Data = Serial_COM2_Rx_Data.hex().strip()
                        Serial_COM2_Rx_Data = Serial_COM2_Rx_Data.decode('utf-8', errors='ignore').strip()
                        #print(Serial_COM2_Rx_Data)
                        if(Serial_COM2_Rx_Data.isdigit()):
                            variablesGlobales.lastDNI_Serial = Serial_COM2_Rx_Data  
                            
                            log.escribeSeparador(hbl.LOGS_hblReporte)
                            log.escribeLineaLog(hbl.LOGS_hblReporte, 
                                                "Datos Serial2 recibidos : " + variablesGlobales.lastDNI_Serial) 
                        elif "Conectado" in Serial_COM2_Rx_Data:
                            log.escribeSeparador(hbl.LOGS_hblReporte)
                            log.escribeLineaLog(hbl.LOGS_hblReporte, 
                                                "Datos Serial2 recibidos : " + "Conectado") 

                        time.sleep(0.03)
    
                except Exception as e:
                
                    exc_type, exc_obj, exc_tb = sys.exc_info() 
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
                    errorExcepcion = "ERROR : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

                    log.escribeSeparador(hbl.LOGS_hblReporte)
                    log.escribeLineaLog(hbl.LOGS_hblReporte, "Error : " + str(errorExcepcion)) 
        
        time.sleep(0.01)
    log.escribeSeparador(hbl.LOGS_hblSerial)
    log.escribeLineaLog(hbl.LOGS_hblSerial, "SERIAL2 STOPED") 
""" --------------------------------------------------------------------------------------------

    inicializacion comunicacion Serial

-------------------------------------------------------------------------------------------- """

def inicializacion(pi2): 
    #auxiliar.EscribirFuncion("inicializacion")

    global pi
 
    pi = pi2

    if hbl.SERIAL_COM1_activado == 1:
 
        try:

            serialHBL = threading.Thread(target=startThreadSerial, name='HBLSerial1')
            serialHBL.setDaemon(False)
            serialHBL.start()   

            log.escribeSeparador(hbl.LOGS_hblSerial)
            log.escribeLineaLog(hbl.LOGS_hblSerial, "Serial1 Start")  
        
        except Exception as e:
              
            exc_type, exc_obj, exc_tb = sys.exc_info() 
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
            errorExcepcion = "ERROR : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

            log.escribeSeparador(hbl.LOGS_hblSerial)
            log.escribeLineaLog(hbl.LOGS_hblSerial, "Error : " + str(errorExcepcion)) 

    if hbl.SERIAL_COM2_activado == 1:
 
        try:

            serialHBL = threading.Thread(target=startThreadSerial2, name='HBLSerial2')
            serialHBL.setDaemon(False)
            serialHBL.start()   

            log.escribeSeparador(hbl.LOGS_hblSerial)
            log.escribeLineaLog(hbl.LOGS_hblSerial, "Serial2 Start")  
        
        except Exception as e:
              
            exc_type, exc_obj, exc_tb = sys.exc_info() 
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
            errorExcepcion = "ERROR : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

            log.escribeSeparador(hbl.LOGS_hblSerial)
            log.escribeLineaLog(hbl.LOGS_hblSerial, "Error : " + str(errorExcepcion))  
      