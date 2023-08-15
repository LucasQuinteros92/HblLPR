
import socket
import datetime
import os
import sys
import requests
import time  
import threading  
import usb.util
import json
from usb.core import find as finddev 

from modulos import log as log
from modulos import hbl as hbl
from modulos import delays as delays
from modulos import conexiones as conexiones
from modulos import auxiliar as auxiliar
from modulos import variablesGlobales as variablesGlobales

global device
global canvas 

""" --------------------------------------------------------------------------------------------


    inicializa HBL


-------------------------------------------------------------------------------------------- """

def inicializacionHBL():
 
    # escribe inicializacion HBL
    log.escribeSeparador(hbl.LOGS_hblCore)
    log.escribeLineaLog(hbl.LOGS_hblCore, "Inicio HBL - " + " v." + hbl.versionHBL) 
    log.escribeLineaLog(hbl.LOGS_hblCore, "Num. Serie : " +  leer_numero_serie()) 
    log.escribeLineaLog(hbl.LOGS_hblCore, "Revision : " +  leer_revision()) 
    log.escribeLineaLog(hbl.LOGS_hblCore, "MAC address eth0 : " + leer_MAC_Address('eth0'))  
    log.escribeLineaLog(hbl.LOGS_hblCore, "MAC address eth0 : " + leer_MAC_Address('wlan0'))  
    log.escribeLineaLog(hbl.LOGS_hblCore, "Temperatura : " + measure_temp()) 
    get_throttled()
   
    print("\n\n*****************************************************")
    print("    _   _ ____  _        ")    
    print("   | | | | __ )| |       ") 
    print("   | |_| |  _ \| |       ") 
    print("   |  _  | |_) | |___    ") 
    print("   |_| |_|____/|_____|   ")  
    print("")
    print(" v.", hbl.versionHBL)  
    print(" Num. Serie : ", leer_numero_serie())
    print(" Revision : ", leer_revision())
    print(" MAC eth0 : ", leer_MAC_Address('eth0'))
    print(" MAC wlan0 : ", leer_MAC_Address('wlan0')) 
    print("")
    print("*****************************************************\n\n")

    # escribe configuracion HBL 
    log.configuracionHBL(hbl.LOGS_hblCore)    

    # realiza un update en el JSON con los valores de la RPI  
    lecturaParametrosHBL()

    # sincroniza reloj segun NTP
    sincronizarHora()
 
 
""" --------------------------------------------------------------------------------------------

    get_throttled - Status del sistema  

    11110000000000001111
    ||||            ||||_ bajo voltaje
    ||||            |||_ frecuencia del cpu al limite 
    ||||            ||_ cpu trabajando forzadamente
    ||||            |_ pico de temperatura activo
    ||||_ ocurrio un bajo voltaje desde el ultimo reset
    |||_ ocurrio un frecuencia del cpu al limite desde el ultimo reset
    ||_ ocurrio un forzado del cpu desde el ultimo reset
    |_ ocurrio un pico de temperatura desde el ultimo reset

-------------------------------------------------------------------------------------------- """

def get_throttled():
 
    throttled = os.popen("vcgencmd get_throttled").readline()
    throttled = throttled.replace("throttled=", "")  
    throttled = throttled.replace("\n", "")  
    throttled = int(throttled, 16)
    numeroBinario = bin(throttled)[2:].zfill(20) 

    if numeroBinario[19] == 1:
        log.escribeSeparador(hbl.LOGS_hblCore) 
        log.escribeLineaLog(hbl.LOGS_hblCore, "ocurrio un pico de temperatura desde el ultimo reset")
    if numeroBinario[18] == 1:
        log.escribeSeparador(hbl.LOGS_hblCore) 
        log.escribeLineaLog(hbl.LOGS_hblCore, "ocurrio un forzado del cpu desde el ultimo reset")
    if numeroBinario[17] == 1:
        log.escribeSeparador(hbl.LOGS_hblCore) 
        log.escribeLineaLog(hbl.LOGS_hblCore, "ocurrio un frecuencia del cpu al limite desde el ultimo reset")
    if numeroBinario[16] == 1:
        log.escribeSeparador(hbl.LOGS_hblCore) 
        log.escribeLineaLog(hbl.LOGS_hblCore, "ocurrio un bajo voltaje desde el ultimo reset")
    if numeroBinario[3] == 1:
        log.escribeSeparador(hbl.LOGS_hblCore) 
        log.escribeLineaLog(hbl.LOGS_hblCore, "pico de temperatura activo")
    if numeroBinario[2] == 1:
        log.escribeSeparador(hbl.LOGS_hblCore) 
        log.escribeLineaLog(hbl.LOGS_hblCore, "cpu trabajando forzadamente")         
    if numeroBinario[1] == 1:
        log.escribeSeparador(hbl.LOGS_hblCore) 
        log.escribeLineaLog(hbl.LOGS_hblCore, "frecuencia del cpu al limite")
    if numeroBinario[0] == 1:
        log.escribeSeparador(hbl.LOGS_hblCore) 
        log.escribeLineaLog(hbl.LOGS_hblCore, "bajo voltaje")    

""" --------------------------------------------------------------------------------------------

    get_throttled - Status del sistema  

    * lee el status del sistema y lo acomoda en un byte (8 bits) para envio al reporte

-------------------------------------------------------------------------------------------- """

def get_throttled_bytes():

    throttled = os.popen("vcgencmd get_throttled").readline()
    throttled = throttled.replace("throttled=", "")  
    throttled = throttled.replace("\n", "")  
    throttled = int(throttled, 16)
    numeroBinario = bin(throttled)[2:].zfill(20) 
    seleccionBytes = numeroBinario[0] + numeroBinario[1] + numeroBinario[2] + numeroBinario[3] + numeroBinario[16] + numeroBinario[17] + numeroBinario[18] + numeroBinario[19]
    
    return seleccionBytes

""" --------------------------------------------------------------------------------------------

    lee los parametros unicos de hbl

    * numero de serie
    * revision
    * mac address Ethernet adaptor

    y lo graba en el json del hbl

-------------------------------------------------------------------------------------------- """

def lecturaParametrosHBL():

    # path del archivo
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    # Leo los parametros de configuracion en el JSON
    with open(os.path.join(__location__ , 'hbl.json'), "r") as f:
        data = json.load(f)

    data["hblCore"]["serialNumber"] = leer_numero_serie()
    data["hblCore"]["revision"] = leer_revision()
    data["hblCore"]["MAC_ethernet"] = leer_MAC_Address('eth0')

    # actualizo los parametros en el JSON y le da formato al mismo
    with open(os.path.join(__location__ , 'hbl.json'), "w") as f:
        json.dump(data, f, indent=4)   

""" --------------------------------------------------------------------------------------------

   leer temperatura del core de la RPI

-------------------------------------------------------------------------------------------- """

def measure_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return (temp.replace("temp=", ""))

""" --------------------------------------------------------------------------------------------

   Retorna la fecha actual del HBL

-------------------------------------------------------------------------------------------- """

def timeNow():
    return str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

""" --------------------------------------------------------------------------------------------

    Retorna la fecha actual del HBL ( otro metodo )

-------------------------------------------------------------------------------------------- """

def getDate():

    p = os.popen("date '+%F %T'") 
    line = p.readline() 
    return line 

""" --------------------------------------------------------------------------------------------

    Sincroniza la fecha del HBL con el servidor NTP  

-------------------------------------------------------------------------------------------- """

def sincronizarHora():
    
    try:
        # escribe en el archivo de seleccion del servidor el indicado en el json del HBL
        parametrosNet = ['# Server para sincronizacion del reloj', ' ' , '[Time]', 'NTP=' + hbl.HBLCORE_NTP, ' ']
        auxiliar.append_multiple_lines('/etc/systemd/timesyncd.conf', parametrosNet, "w+") 

        # activa la sincronizacion con el servidor NTP y hace un reload del daemon
        os.system("sudo systemctl restart systemd-timesyncd.service")  
        os.system("sudo timedatectl set-ntp true") 
        os.system("sudo systemctl daemon-reload") 

        log.escribeSeparador(hbl.LOGS_hblCore) 
        log.escribeLineaLog(hbl.LOGS_hblCore, "Sincronizada la fecha del HBL con el servidor NTP") 

    except Exception as e:  
    
        exc_type, exc_obj, exc_tb = sys.exc_info() 
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
        errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 
    
        log.escribeSeparador(hbl.LOGS_hblCore)
        log.escribeLineaLog(hbl.LOGS_hblCore, "Error : " + str(errorExcepcion))  

""" --------------------------------------------------------------------------------------------

   leer los numeros de serie / revision / mac address de la RPI

   ej:

    # MAC Address del Ethernet adapter
    ethtool --show-permaddr eth0    
    # res : dc:a6:32:52:2d:ee

    # otro metodo :
    $ vcgencmd otp_dump | grep '65:' 
    $ vcgencmd otp_dump | grep '64:' 

    # MAC Address del WiFi adapter
    ethtool --show-permaddr wlan0   

    # averiguar el numero de serie de la RPI
    $ vcgencmd otp_dump | grep '28:' 
    # res : 28:f9976413

    # averiguar la revision de la RPI (2G, 4G, etc)
    $ vcgencmd otp_dump | grep '30:' 
    # res : 30:00c03112

-------------------------------------------------------------------------------------------- """

def leer_numero_serie():
    numeroSerie = os.popen("vcgencmd otp_dump | grep '28:'").readline()
    numeroSerie = numeroSerie.replace("\n", "")
    return (numeroSerie.replace("28:", ""))

def leer_revision():
    revision = os.popen("vcgencmd otp_dump | grep '30:'").readline()
    revision = revision.replace("\n", "")
    return (revision.replace("30:", ""))

def leer_MAC_Address(interfase):
    macAddress = os.popen("ethtool --show-permaddr " + interfase).readline()
    macAddress = macAddress.replace("\n", "")
    return (macAddress.replace("Permanent address: ", "")) 

""" --------------------------------------------------------------------------------------------

   leer % de uso de CPU

-------------------------------------------------------------------------------------------- """

def usoCPU(numeroCPU):  

    if numeroCPU == 0 : 
        line = os.popen("cat /proc/stat | grep '^cpu0'").readline() 
    elif numeroCPU == 1 : 
        line = os.popen("cat /proc/stat | grep '^cpu1'").readline() 
    elif numeroCPU == 2 : 
        line = os.popen("cat /proc/stat | grep '^cpu2'").readline() 
    elif numeroCPU == 3 : 
        line = os.popen("cat /proc/stat | grep '^cpu3'").readline() 
    else : 
        line = os.popen("cat /proc/stat | grep '^cpu'").readline() 

    valores = line.split()
    totalCPU = int(valores[1]) + int(valores[2]) + int(valores[3]) + int(valores[4]) + int(valores[5]) + int(valores[6]) + int(valores[7]) + int(valores[8]) + int(valores[9]) + int(valores[10])     
    idleCPU = (int(valores[4]) * 100 ) / totalCPU # valor del CPU sin uso teniendo en cuenta todos los procesos activos
     
    CPUenUso = format(100 - idleCPU, ".2f")

    return str(CPUenUso)

""" --------------------------------------------------------------------------------------------

    Return RAM information (unit=kb) in a list                                        
        Index 0: total RAM                                                                
        Index 1: used RAM                                                                 
        Index 2: free RAM  

-------------------------------------------------------------------------------------------- """
                                                
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            valores = line.split()[1:4]
            ram = str(format((float(valores[1]) * 100) / float(valores[0]), ".2f")) 
            return(ram)       

""" --------------------------------------------------------------------------------------------

    Return information about disk space as a list (unit included)                     
        Index 0: total disk space                                                         
        Index 1: used disk space                                                          
        Index 2: remaining disk space                                                     
        Index 3: percentage of disk used 

-------------------------------------------------------------------------------------------- """

def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            valores = line.split()[1:5]
            spaceDisk = valores[3]
            spaceDisk = spaceDisk.replace("%", "")
            spaceDisk = str(format(float(spaceDisk), ".2f")) 
            return spaceDisk      

""" --------------------------------------------------------------------------------------------

    Retorna la version del bootloader instalada en el HBL

-------------------------------------------------------------------------------------------- """

def getBootloaderVersion():

    try:

        p = os.popen("vcgencmd bootloader_version") 
        line = p.readline() 
        return(line)  
    
    except Exception as e:  

        exc_type, exc_obj, exc_tb = sys.exc_info() 
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
        errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

        log.escribeSeparador(hbl.LOGS_hblCore)
        log.escribeLineaLog(hbl.LOGS_hblCore, "Error : " + str(errorExcepcion)) 

        return "error getBootloaderVersion"


""" --------------------------------------------------------------------------------------------

    Retorna los nombres de los volumenes usb    

-------------------------------------------------------------------------------------------- """

def getVolumeNames(drive):

    try:
        p = os.popen("sudo lsblk -o UUID,NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,MODEL | grep '" + drive + "'")     
        line = p.readline()  
        valores = line.split()
        return valores    
    
    except Exception as e:  

        exc_type, exc_obj, exc_tb = sys.exc_info() 
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
        errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

        log.escribeSeparador(hbl.LOGS_hblCore)
        log.escribeLineaLog(hbl.LOGS_hblCore, "Error : " + str(errorExcepcion)) 
        
        return "error getVolumeNames"

""" --------------------------------------------------------------------------------------------

   inicializa Oled

-------------------------------------------------------------------------------------------- """

def inicializaoled():

    global device
    global canvas

    if hbl.HBLCORE_hblDisplay_activado == 1:

        from modulos.luma.core.interface.serial import i2c
        from modulos.luma.oled.device import sh1106
        from modulos.luma.core.render import canvas 

        try:

            serial = i2c(port=1, address=0x3C)
            device = sh1106(serial)

        except Exception as e:  
    
            exc_type, exc_obj, exc_tb = sys.exc_info() 
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
            errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 
        
            log.escribeSeparador(hbl.LOGS_hblCore)
            log.escribeLineaLog(hbl.LOGS_hblCore, "Error : " + str(errorExcepcion)) 
  
""" --------------------------------------------------------------------------------------------

   oledRefresh

-------------------------------------------------------------------------------------------- """
 
def oledRefresh():

    global device
    global canvas

    if hbl.HBLCORE_hblDisplay_activado == 1:

        try:

            if hbl.HBLCORE_hblDisplay_modo == 1: 

                if hbl.pantallaOled == 1:                
                    hbl.pantallaOled = 2

                    fechaHora = str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
                    temperatura = "T: " + measure_temp()
                        
                    ip_eth0 = "eth0: " + conexiones.get_ip_address('eth0') 
                    ip_wlan0 = "wlan0: " + conexiones.get_ip_address('wlan0')  

                    # lee la cantidad de bytes transferidos en la interfase eth0, lo convierte a Mb luego 
                    # convierte ese valor a float con 2 decimales y luego a string
                    tx_bytes_eth0 = str(format(int(conexiones.get_bytes_interface_tx('eth0')) / 1024768, ".2f")) 
                    rx_bytes_eth0 = str(format(int(conexiones.get_bytes_interface_rx('eth0')) / 1024768, ".2f")) 

                    # lee la cantidad de bytes transferidos en la interfase wlan0, lo convierte a Mb luego 
                    # convierte ese valor a float con 2 decimales y luego a string
                    tx_bytes_wlan0 = str(format(int(conexiones.get_bytes_interface_tx('wlan0')) / 1024768, ".2f")) 
                    rx_bytes_wlan0 = str(format(int(conexiones.get_bytes_interface_rx('wlan0')) / 1024768, ".2f"))  

                    with canvas(device) as draw:  
                        
                        # fecha / hora
                        size = draw.textsize(fechaHora) 
                        draw.text(((device.width - size[0])/2, 0), fechaHora, fill="white") 

                        # temperatura
                        size = draw.textsize(temperatura) 
                        draw.text(((device.width - size[0])/2, 10), temperatura, fill="white")  

                        # ip eth0
                        size = draw.textsize(ip_eth0) 
                        draw.text(((device.width - size[0])/2, 25), ip_eth0, fill="white") 

                        size = draw.textsize(tx_bytes_eth0) 
                        draw.text((0, 35), tx_bytes_eth0, fill="white") 
                        
                        size = draw.textsize(rx_bytes_eth0) 
                        draw.text((60, 35), rx_bytes_eth0 , fill="white") 

                        # ip wlan0
                        size = draw.textsize(ip_wlan0) 
                        draw.text(((device.width - size[0])/2, 45), ip_wlan0, fill="white")

                        size = draw.textsize(tx_bytes_wlan0) 
                        draw.text((0, 55), tx_bytes_wlan0, fill="white") 
                        
                        size = draw.textsize(rx_bytes_wlan0) 
                        draw.text((60, 55), rx_bytes_wlan0, fill="white")   
                    
                elif hbl.pantallaOled == 2:
                    hbl.pantallaOled = 1 

                    fechaHora = str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
                    temperatura = "T: " + measure_temp()

                    usoProcesador = "CPU : " + usoCPU(9) + "%" 
                    usoRAM = "RAM : " + getRAMinfo() + "%" 
                    spaceDisk = "DSK: " + getDiskSpace() + "%"
                    
                    with canvas(device) as draw:  
                        
                        # fecha / hora
                        size = draw.textsize(fechaHora) 
                        draw.text(((device.width - size[0])/2, 0), fechaHora, fill="white") 

                        # temperatura
                        size = draw.textsize(temperatura) 
                        draw.text(((device.width - size[0])/2, 10), temperatura, fill="white")  

                        # % CPU
                        size = draw.textsize(usoProcesador) 
                        draw.text(((device.width - size[0])/2, 35), usoProcesador, fill="white")  

                        # RAM
                        size = draw.textsize(usoRAM) 
                        draw.text(((device.width - size[0])/2, 45), usoRAM, fill="white") 

                        # DISK
                        size = draw.textsize(spaceDisk) 
                        draw.text(((device.width - size[0])/2, 55), spaceDisk, fill="white") 
            
            elif hbl.HBLCORE_hblDisplay_modo == 2: 
                pass
        
        except Exception as e:  
    
            exc_type, exc_obj, exc_tb = sys.exc_info() 
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
            errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 
        
            log.escribeSeparador(hbl.LOGS_hblCore)
            log.escribeLineaLog(hbl.LOGS_hblCore, "Error : " + str(errorExcepcion)) 

""" --------------------------------------------------------------------------------------------

   * heartBeat

   * reset programado del hbl

-------------------------------------------------------------------------------------------- """

def heartBeat(pi):

    try:
        
        # heartBeat
        pi.write(hbl.DIG_led2, hbl.OFF)    
        delays.ms(500)      
        pi.write(hbl.DIG_led2, hbl.ON)  
        delays.ms(500)

        # chequea el valor del tamper si esta activado
        if hbl.HBLCORE_tamper_activado == 1: 
            pass

        # reset programado del hbl
        if hbl.HBLCORE_reset_resetActivado == 1:

            variablesGlobales.HBLCORE_contadorReset = variablesGlobales.HBLCORE_contadorReset + 1 
            log.escribeLineaLog(hbl.LOGS_hblCore , "Reset Programado Activado : Valor contador reset : " + str(variablesGlobales.HBLCORE_contadorReset))

            if variablesGlobales.HBLCORE_contadorReset >= hbl.HBLCORE_reset_tiempoReset: 
                log.escribeLineaLog(hbl.LOGS_hblCore ,"Reset HBL...")
                os.system("sudo reboot")
       
    except Exception as e:  

        exc_type, exc_obj, exc_tb = sys.exc_info() 
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
        errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 
    
        log.escribeSeparador(hbl.LOGS_hblCore)
        log.escribeLineaLog(hbl.LOGS_hblCore, "Error : " + str(errorExcepcion)) 


""" --------------------------------------------------------------------------------------------


    encenderLed


-------------------------------------------------------------------------------------------- """

def encenderLed(pi, led, tiempo):

    try:
        if led == 1: 
         
            # led rojo
            pi.write(hbl.DIG_led1, hbl.OFF)    
            delays.ms(tiempo) 
            pi.write(hbl.DIG_led1, hbl.ON)    
            delays.ms(tiempo) 
        
        elif led == 2:

            # led azul
            pi.write(hbl.DIG_led2, hbl.OFF)    
            delays.ms(tiempo) 
            pi.write(hbl.DIG_led2, hbl.ON)    
            delays.ms(tiempo) 
  
        elif led == 3:

            # led 
            pi.write(hbl.DIG_led3, hbl.OFF)    
            delays.ms(tiempo)
            pi.write(hbl.DIG_led3, hbl.ON)    
            delays.ms(tiempo)   

    except Exception as e:  

        exc_type, exc_obj, exc_tb = sys.exc_info() 
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
        errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 
    
        log.escribeSeparador(hbl.LOGS_hblCore)
        log.escribeLineaLog(hbl.LOGS_hblCore, "Error : " + str(errorExcepcion)) 

""" --------------------------------------------------------------------------------------------


    checkLedsBuzzer


-------------------------------------------------------------------------------------------- """

def checkLedsBuzzer(pi):

    try:

        # Buzzer
        pi.write(hbl.DIG_buzzer, hbl.OFF)    
        delays.ms(500)  
        pi.write(hbl.DIG_buzzer, hbl.ON)  
        delays.ms(500) 

        # led rojo
        pi.write(hbl.DIG_led1, hbl.OFF)    
        delays.ms(200) 
        pi.write(hbl.DIG_led1, hbl.ON)    
        delays.ms(200) 

        # led azul
        pi.write(hbl.DIG_led2, hbl.OFF)    
        delays.ms(200) 
        pi.write(hbl.DIG_led2, hbl.ON)    
        delays.ms(200) 

        # led  
        pi.write(hbl.DIG_led3, hbl.OFF)    
        delays.ms(200)
        pi.write(hbl.DIG_led3, hbl.ON)    
        delays.ms(200)   

    except Exception as e:  

        exc_type, exc_obj, exc_tb = sys.exc_info() 
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
        errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 
    
        log.escribeSeparador(hbl.LOGS_hblCore)
        log.escribeLineaLog(hbl.LOGS_hblCore, "Error : " + str(errorExcepcion)) 