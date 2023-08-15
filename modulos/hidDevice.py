
import usb.core
import usb.util
import sys  
import time
import datetime
import usb
import threading
import json
import os
import json

from modulos import log as log
from modulos import hbl as hbl
from modulos import delays as delays
from modulos import i2cDevice as i2cDevice

from modulos.encoderWiegand import Encoder
 
"""

ID's de dispositivos utilizados:

    Teclado generico

        Vendor ID  : 0xb6ce
        Product ID : 0x0001
        Endpoint   : 0x81
        BufferSize : 20
        Timeout    : 200

    Lector DNI

        Vendor ID  : 0x05e0
        Product ID : 0x1200
        Endpoint   : 0x81
        BufferSize : 20
        Timeout    : 200
    
    Lector ZK

        Vendor ID  : 0xffff
        Product ID : 0x0035  
        Endpoint   : 0x81
        BufferSize : 20
        Timeout    : 2000

 
    Honeywell Imaging & Mobility
    7580

        Vendor ID  : 0x0c2e
        Product ID : 0x0be1  
        Endpoint   : 0x84
        BufferSize : 20
        Timeout    : 200
  
"""

device = ()
threads = []

global c
global pi

global posicionCaracter   
global cantidadCaracteres  
global DNICompleto 
global DNICompletado 
  
""" --------------------------------------------------------------------------------------------


   listarUSBDevices


-------------------------------------------------------------------------------------------- """

def listarUSBDevices():

    dev = usb.core.find(find_all=True)
   
    for cfg in dev:
        sys.stdout.write('Decimal VendorID=' + str(cfg.idVendor) + ' & ProductID=' + str(cfg.idProduct) + '\n')
        sys.stdout.write('Hexadecimal VendorID=' + hex(cfg.idVendor) + ' & ProductID=' + hex(cfg.idProduct) + '\n\n')
  
""" --------------------------------------------------------------------------------------------


   detachResetHID


-------------------------------------------------------------------------------------------- """

def detachResetHID(dispositivo, numero):
   
    if dispositivo[numero].is_kernel_driver_active(0):
        try:
            if hbl.DEBUG == 1:  
                print("Detaching kernel driver")

            dispositivo[numero].detach_kernel_driver(0)

            if hbl.DEBUG == 1:  
                print("kernel driver detached")

        except usb.core.USBError as e:
            sys.exit("Could not detach kernel driver: %s" % str(e))
    else:
        if hbl.DEBUG == 1:  
            print("no kernel driver attached") 
    
    usb.util.dispose_resources(dispositivo[numero])

    dispositivo[numero].reset()


def detachHID(device):
    
    for k in range(len(device)):
        detachResetHID(device, k) 
 
""" --------------------------------------------------------------------------------------------


   tabla decodificador HID


-------------------------------------------------------------------------------------------- """

def decodificadorHID(datos):

    # Caracteres numericos + Enter + Cancel
    if datos[0] == 0 and datos[2] == 30: 
        return 1
    elif datos[0] == 0 and datos[2] == 31:
        return 2
    elif datos[0] == 0 and datos[2] == 32:
        return 3
    elif datos[0] == 0 and datos[2] == 33:
        return 4
    elif datos[0] == 0 and datos[2] == 34:
        return 5
    elif datos[0] == 0 and datos[2] == 35:
        return 6
    elif datos[0] == 0 and datos[2] == 36:
        return 7
    elif datos[0] == 0 and datos[2] == 37:
        return 8
    elif datos[0] == 0 and datos[2] == 38:
        return 9
    elif datos[0] == 0 and datos[2] == 39:
        return 0
    elif datos[0] == 0 and datos[2] == 40:
        return "Enter"
    elif datos[0] == 0 and datos[2] == 41:
        return "Esc"
    elif datos[0] == 0 and datos[2] == 42:
        return "Cancel"
    elif datos[0] == 0 and datos[2] == 43:
        return "Tab"  
    elif datos[0] == 0 and datos[2] == 44:
        return " "
    elif datos[0] == 0 and datos[2] == 45:
        return "- _"
    elif datos[0] == 0 and datos[2] == 46:
        return "= +"
    elif datos[0] == 0 and datos[2] == 47:
        return "[{"
    elif datos[0] == 0 and datos[2] == 48:
        return "]}`"
    elif datos[0] == 0 and datos[2] == 49:
        return " "
    elif datos[0] == 0 and datos[2] == 50:
        return "Euro1"
    elif datos[0] == 0 and datos[2] == 51:
        return ": :"  
    elif datos[0] == 0 and datos[2] == 52:
        return " "
    elif datos[0] == 0 and datos[2] == 53:
        return " "
    elif datos[0] == 0 and datos[2] == 54:
        return " "
    elif datos[0] == 0 and datos[2] == 55:
        return " "
    elif datos[0] == 0 and datos[2] == 56:
        return " "
    elif datos[0] == 0 and datos[2] == 57:
        return "Caps Lock"
    elif datos[0] == 0 and datos[2] == 58:
        return "F1"
    elif datos[0] == 0 and datos[2] == 59:
        return "F2"  
    elif datos[0] == 0 and datos[2] == 60:
        return "F3"
    elif datos[0] == 0 and datos[2] == 61:
        return "F4"
    elif datos[0] == 0 and datos[2] == 62:
        return "F5"
    elif datos[0] == 0 and datos[2] == 63:
        return "F6"
    elif datos[0] == 0 and datos[2] == 64:
        return "F7"
    elif datos[0] == 0 and datos[2] == 65:
        return "F8"
    elif datos[0] == 0 and datos[2] == 66:
        return "F9"
    elif datos[0] == 0 and datos[2] == 67:
        return "F10"
    elif datos[0] == 0 and datos[2] == 68:
        return "F11"  
    elif datos[0] == 0 and datos[2] == 69:
        return "F12"
    elif datos[0] == 0 and datos[2] == 70:
        return "Print Screen"
    elif datos[0] == 0 and datos[2] == 71:
        return "Scroll lock"
    elif datos[0] == 0 and datos[2] == 72:
        return "Break"

    # Caracteres Letras + Caracteres especiales
    elif datos[0] == 2 and datos[2] == 4: 
        return "A"
    elif datos[0] == 2 and datos[2] == 5:
        return "B"
    elif datos[0] == 2 and datos[2] == 6:
        return "C"
    elif datos[0] == 2 and datos[2] == 7:
        return "D"
    elif datos[0] == 2 and datos[2] == 8:
        return "E"
    elif datos[0] == 2 and datos[2] == 9:
        return "F"
    elif datos[0] == 2 and datos[2] == 10:
        return "G"
    elif datos[0] == 2 and datos[2] == 11:
        return "H"
    elif datos[0] == 2 and datos[2] == 12:
        return "I"
    elif datos[0] == 2 and datos[2] == 13:
        return "J"
    elif datos[0] == 2 and datos[2] == 14:
        return "K"
    elif datos[0] == 2 and datos[2] == 15:
        return "L"
    elif datos[0] == 2 and datos[2] == 16:
        return "M"
    elif datos[0] == 2 and datos[2] == 17:
        return "N"
    elif datos[0] == 2 and datos[2] == 18:
        return "O"
    elif datos[0] == 2 and datos[2] == 19:
        return "P"
    elif datos[0] == 2 and datos[2] == 20:
        return "Q"
    elif datos[0] == 2 and datos[2] == 21:
        return "R"
    elif datos[0] == 2 and datos[2] == 22:
        return "S"
    elif datos[0] == 2 and datos[2] == 23:
        return "T"
    elif datos[0] == 2 and datos[2] == 24:
        return "U"
    elif datos[0] == 2 and datos[2] == 25:
        return "V"
    elif datos[0] == 2 and datos[2] == 26:
        return "w"
    elif datos[0] == 2 and datos[2] == 27:
        return "X"
    elif datos[0] == 2 and datos[2] == 28:
        return "Y"
    elif datos[0] == 2 and datos[2] == 29:
        return "Z"
    elif datos[0] == 2 and datos[2] == 31:
        return "@"
    else:
        return "Err" 

""" --------------------------------------------------------------------------------------------


   class dispositivosHID


-------------------------------------------------------------------------------------------- """ 

class dispositivosHID:

    def __init__(self, pi):
        self._running = True 
        self.pi = pi
    
    def terminate(self):
        self._running = False
    
    def run(self, dispositivo, numero, bufferSize, timeout, endpoint):

        stringLeido = "" 

        posicionCaracter = 5        
        cantidadCaracteres = 0
        DNICompleto = ""
        DNICompletado = False

        while self._running == True:
    
            try:

                # Teclado Generico USB 
                # Lector DNI 

                byteRecibido = dispositivo[numero].read(endpoint, bufferSize, timeout)  
                caracterLeido = decodificadorHID(byteRecibido)   
                 
                log.escribeLineaLog(hbl.LOGS_hblhidDevice, "USB Port : " + str(dispositivo[numero].port_number) + "  /  Caracter leido : " + str(caracterLeido))   
                
                if hbl.FUNC_modo == 5: 

                    if caracterLeido != "Err":   
                        if caracterLeido != "Enter":     
                            stringLeido += str(caracterLeido) 
                            print(stringLeido)
                        else:
                            stringLeido = stringLeido + "@" + str(dispositivo[numero].port_number)

                            # escribe separador + fecha + hora
                            log.escribeSeparador(hbl.LOGS_hblhidDevice) 
                            log.escribeLineaLog(hbl.LOGS_hblhidDevice,"Valor : " + str(stringLeido)) 

                            # recarga los parametros de hbl.json por actualizacion
                            # hbl.cargarParametros('hbl.json')                    
                            
                            #  Funcionamiento del hbl segun modo seleccionado
                            #
                            #   5 : lector DNI HID -> wiegand 34
                            # 
                            #   dni nuevo ej:
                            #                00542631492"OCHOA DE EGUILEOR CALIGIURI"AGUSTINA SOFIA"F"41780151"C"29-05-1999"04-04-2018"276 
                            #   dni viejo ej:
                            #                "38464428    "A"1"PAN PERALTA"NICOLAS"ARGENTINA"19-08-1994"M"22-06-2011"00056089158"7059 "22-06-2026"378"0"
                            #                ILRÑ2.01 CÑ110613.02 )No Cap.="UNIDAD ·09 ÇÇ S-NÑ 0040:2008::0009
                      
                            # Parseo valor del dni en el string completo
                            stringSplit=stringLeido.split('@')
                        
                            log.escribeLineaLog(hbl.LOGS_hblhidDevice,"SPLIT : " + str(stringSplit)) 

                            tamanioLista = len(stringSplit)

                            log.escribeLineaLog(hbl.LOGS_hblhidDevice,"Tamaño lista : " + str(tamanioLista))  

                            # extraigo DNI
                            if tamanioLista > 12 :
                                dni = stringSplit[1]
                            else:
                                dni = stringSplit[4]  

                            # Dni binario completo en 32 bits
                            # convierte el valor del dni a binario
                            # y completa con 0 hasta llegar a 32 bits
                            try:

                                dniBinario = bin(int(dni))[2:].zfill(32) 
                                
                                log.escribeLineaLog(hbl.LOGS_hblhidDevice,"DNI bin : " + str(dniBinario))  
    
                                # parte alta del binario 
                                dinBinarioAlta = dniBinario[:-16]
                                
                                log.escribeLineaLog(hbl.LOGS_hblhidDevice,"DNI Alta bin : " + str(dinBinarioAlta)) 

                                dinIntegerAlta = int(dinBinarioAlta, 2) 

                                log.escribeLineaLog(hbl.LOGS_hblhidDevice,"DNI Alta int : " + str(dinIntegerAlta)) 

                                # cuenta cantidad de bits en 1 en esta parte para calcular la paridad Par (EVEN)
                                cantBitsParteAlta = 0

                                while (dinIntegerAlta): 
                                    cantBitsParteAlta += dinIntegerAlta & 1
                                    dinIntegerAlta >>= 1
                                
                                log.escribeLineaLog(hbl.LOGS_hblhidDevice,"Cant. 1 parte alta : " + str(cantBitsParteAlta))     

                                # parte baja del binario
                                dinBinarioBaja = dniBinario[16:]   
                                
                                log.escribeLineaLog(hbl.LOGS_hblhidDevice,"DNI Baja : " + str(dinBinarioBaja)) 

                                dinIntegerBaja = int(dinBinarioBaja, 2)
                                
                                log.escribeLineaLog(hbl.LOGS_hblhidDevice,"DNI Baja int : " + str(dinIntegerBaja)) 

                                # cuenta cantidad de bits en 1 en esta parte para calcular la paridad Impar (ODD)
                                cantBitsParteBaja = 0

                                while (dinIntegerBaja): 
                                    cantBitsParteBaja += dinIntegerBaja & 1
                                    dinIntegerBaja >>= 1
                                                                
                                log.escribeLineaLog(hbl.LOGS_hblhidDevice,"Cant. 1 parte baja : " + str(cantBitsParteBaja))

                                # agrego los bits de paridad al binario del dni para completar el codigo wiegand antes de enviarlo
                                dniToWiegand = ""

                                # si el numero es par
                                if (cantBitsParteAlta % 2) == 0:   
                                    dniToWiegand = "0" + dniBinario
                                else:  
                                    dniToWiegand = "1" + dniBinario 
                                
                                # si el numero es impar
                                if (cantBitsParteBaja % 2) == 1:   
                                    dniToWiegand = dniToWiegand + "0" 
                                else:  
                                    dniToWiegand = dniToWiegand + "1"  
                                
                                log.escribeLineaLog(hbl.LOGS_hblhidDevice,"WIEGAND COMPLETO: " + str(dniToWiegand)) 

                                # envio codigo wiegand
                                Encoder.encoderWiegandBits(dniToWiegand, self.pi, hbl.WD_port1_pin_WD0, hbl.WD_port1_pin_WD1) 

                            except Exception as inst:

                                log.escribeLineaLog(hbl.LOGS_hblhidDevice, "Error : " + str(inst))

                # 
                #                      
                #   En el caso del modo 7, va a tomar el valor del DNI, lo valida y lo envia por TCP
                #
                #

                elif hbl.FUNC_modo == 7:

                    # Enciende el backlight - muestra el texto en la primer linea
                    i2cDevice.lcd2.put_line(0, "   Ingrese el DNI   ")
                                                  
                    if caracterLeido != "Enter" and caracterLeido != "Cancel" and caracterLeido != "Err":
                      
                        if cantidadCaracteres < 9:

                            if cantidadCaracteres == 0 and caracterLeido == "0":
                                # si el primer caracter es un 0 no lo toma
                                # sino hace el flujo del programa
                                log.escribeLineaLog(hbl.LOGS_hblhidDevice, "Msg : primer caracter del DNI no puede ser 0")
                                pass
                            else:
                                i2cDevice.lcd2.move_to(2, posicionCaracter)
                                i2cDevice.lcd2.put_str(str(caracterLeido))
                                DNICompleto += str(caracterLeido)
                                cantidadCaracteres = cantidadCaracteres + 1 
                                posicionCaracter = posicionCaracter + 1    

                    elif caracterLeido == "Enter":

                        if cantidadCaracteres < 7:
                            log.escribeLineaLog(hbl.LOGS_hblhidDevice, "Msg : error en el DNI - " + str(DNICompleto))
                            i2cDevice.lcd2.move_to(3, 0)
                            i2cDevice.lcd2.put_str("   Error en el DNI  ")
                            time.sleep(3)
                            i2cDevice.lcd2.move_to(2, 0)
                            i2cDevice.lcd2.put_str("                    ")
                            i2cDevice.lcd2.move_to(3, 0)
                            i2cDevice.lcd2.put_str("                    ")
                            cantidadCaracteres = 0
                            posicionCaracter = 5    
                            DNICompleto = ""                       

                        if cantidadCaracteres > 6 and cantidadCaracteres < 10:
                            log.escribeLineaLog(hbl.LOGS_hblhidDevice, "Msg : enviando DNI...")
                            i2cDevice.lcd2.move_to(3, 0)
                            i2cDevice.lcd2.put_str("  Enviando DNI ...  ")
                            time.sleep(3)
                            i2cDevice.lcd2.move_to(2, 0)
                            i2cDevice.lcd2.put_str("                    ")
                            i2cDevice.lcd2.move_to(3, 0)
                            i2cDevice.lcd2.put_str("                    ")
                            cantidadCaracteres = 0
                            posicionCaracter = 5
                            print(DNICompleto)
                            DNICompletado = True                                                  
                                            
                    elif caracterLeido == "Cancel":
                        if cantidadCaracteres > 0:
                            posicionCaracter = posicionCaracter - 1
                            i2cDevice.lcd2.move_to(2, posicionCaracter)
                            i2cDevice.lcd2.put_str(" ")
                            cantidadCaracteres = cantidadCaracteres - 1
                            DNICompleto = DNICompleto[:-1]
                   
                    elif caracterLeido == "Err":
                        pass

                    if DNICompletado == True:
 
                        m = {"id" : "1", "dni" : DNICompleto } 
                        jsonEnvio = json.dumps(m)

                        log.escribeLineaLog(hbl.LOGS_hblhidDevice, "jsonEnvio : " + str(jsonEnvio))
                        DNICompletado = False
                        DNICompleto = ""
                           
                            
                # blanqueo de string
                stringLeido = ""                                                

                byteRecibido = None    
                            
            except usb.core.USBError as e: 
                
                if e.args == ('Operation timed out',):
                    log.escribeLineaLog(hbl.LOGS_hblhidDevice,"Error : Operation timed out")
                    continue

""" --------------------------------------------------------------------------------------------


   threadCount
   

-------------------------------------------------------------------------------------------- """ 

def threadCount():

    global c 
    print(threading.active_count()) 

                
""" --------------------------------------------------------------------------------------------


   getData

    * acceso a los dispositivos HID y lanzamiento threads


-------------------------------------------------------------------------------------------- """ 

def getData(vendor_ID, product_ID, bufferSize, timeout, endpoint):

    global c
    global pi
 
    device = tuple(usb.core.find(find_all=True, idVendor=vendor_ID, idProduct=product_ID))
     
    if len(device) == 0:
        log.escribeLineaLog(hbl.LOGS_hblhidDevice, "Disp HID / vendor_ID: " + str(vendor_ID) + " / product_ID: " + str(product_ID) + " no encontrado!")
        return
    
    # lectura de dispositivos
    log.escribeLineaLog(hbl.LOGS_hblhidDevice, "Disp. HID: " + str(len(device)) + " / vendor_ID: " + str(vendor_ID) + " / product_ID: " + str(product_ID))

    # detach devices HID
    detachHID(device)
    detachHID(device)
      
    for i in range(len(device)):
        c = dispositivosHID(pi)
        t = threading.Thread(target=c.run, args=(device, i, bufferSize, timeout, int(endpoint, 0)))
        threads.append(t)
        t.start() 

""" --------------------------------------------------------------------------------------------


   inicializacion dispositivos HID


-------------------------------------------------------------------------------------------- """ 

def inicializacion(pi2):
    
    global pi
 
    pi = pi2

    if hbl.HID_device1_activado == 1: 
        getData(int(hbl.HID_device1_vendor_ID, 0), int(hbl.HID_device1_product_ID, 0), hbl.HID_device1_bufferSize, hbl.HID_device1_timeout, hbl.HID_device1_endpoint) 
  
    if hbl.HID_device2_activado == 1: 
        getData(int(hbl.HID_device2_vendor_ID, 0), int(hbl.HID_device2_product_ID, 0), hbl.HID_device2_bufferSize, hbl.HID_device2_timeout, hbl.HID_device2_endpoint) 

    if hbl.HID_device3_activado == 1: 
        getData(int(hbl.HID_device3_vendor_ID, 0), int(hbl.HID_device3_product_ID, 0), hbl.HID_device3_bufferSize, hbl.HID_device3_timeout, hbl.HID_device3_endpoint) 
 
    if hbl.HID_device4_activado == 1: 
        getData(int(hbl.HID_device4_vendor_ID, 0), int(hbl.HID_device4_product_ID, 0), hbl.HID_device4_bufferSize, hbl.HID_device4_timeout, hbl.HID_device4_endpoint) 
     
 