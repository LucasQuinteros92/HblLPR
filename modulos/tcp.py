
import socket
import sys 
import datetime
import time  

import modulos.delays
import modulos.hbl
import modulos.log

global sock
 
""" --------------------------------------------------------------------------------------------

   iniciar conexion TCP

-------------------------------------------------------------------------------------------- """

def iniciarConexion():
    
    global sock

    if hbl.TCP_serverDefault_activado == 1: 

        # Crea un socket TCP/IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        # Conecta el socket al puerto del servidor que esta escuchando
        server_address = (hbl.TCP_serverDefault_ip, hbl.TCP_serverDefault_port) 
        
        log.escribeSeparador(hbl.LOGS_hblTcp) 
        log.escribeLineaLog(hbl.LOGS_hblTcp, "Conectando a " + str(server_address[0]) + " / puerto " + str(server_address[1])) 
        
        # si los intentos es 0, prueba una vez y continua, sino entra en el bucle while
        if hbl.TCP_serverDefault_intentosConexion > 0:

            intentos = 0

            while intentos < hbl.TCP_serverDefault_intentosConexion: 

                try:        
                    sock.connect(server_address)
                    break
                except:
                    log.escribeLineaLog(hbl.LOGS_hblTcp, "Reintentando la conexion : " +  str(intentos)) 
                    delays.ms(250)
                    pass

                intentos = intentos + 1
            
            if intentos == hbl.TCP_serverDefault_intentosConexion:
                log.escribeLineaLog(hbl.LOGS_hblTcp, "Error conexion") 
                return 0
            else:
                log.escribeLineaLog(hbl.LOGS_hblTcp, "Conectado")    
                return 1
        
        else:

            try:        
                sock.connect(server_address)
                log.escribeLineaLog(hbl.LOGS_hblTcp, "Conectado") 
                return 1            
            except:
                log.escribeLineaLog(hbl.LOGS_hblTcp, "Error conexion con el servidor")
                return 0 

 
""" --------------------------------------------------------------------------------------------

   envio datos id por TCP

-------------------------------------------------------------------------------------------- """

def envioTCP(id):

    global sock  

    envioOK = 0
   
    try:
        sock.sendall(bytes(str(id), encoding = "utf-8")) 
        log.escribeLineaLog(hbl.LOGS_hblTcp, "Envio OK")
        sock.close() 
        envioOK = 1

    except:
        log.escribeLineaLog(hbl.LOGS_hblTcp, "Error en el envio")
        sock.close() 
        envioOK = 0
    
    return envioOK
        



    
