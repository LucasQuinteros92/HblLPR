 
from modulos import hbl as hbl
from modulos import hblCore as hblCore
from modulos import log as log


""" --------------------------------------------------------------------------------------------

    chequeo si estan presentes las dos unidades, si tienen otros nombres 
    se los cambia para que ya queden definidas

-------------------------------------------------------------------------------------------- """

def checkNombreVolumenes():

    # Separados en log
    log.escribeSeparador(hbl.LOGS_hblRedundancia)
    log.escribeLineaLog(hbl.LOGS_hblRedundancia, "Chequeo nombre de unidades ...") 

    # realiza un recorrido por las unidades de almacenamiento conectadas
    for x in range(ord(hbl.REDUNDANCIA_primeraLetraUnidad), ord(hbl.REDUNDANCIA_ultimaLetraUnidad) + 1):

        for i in range(int(hbl.REDUNDANCIA_primeraParticion), int(hbl.REDUNDANCIA_ultimaParticion) + 1):

            rst = hblCore.getVolumeNames("sd" + chr(x) + str(i))             

            # chequea si la lista tiene contenido para realizar la lectura de los elementos
            if rst:
              
                log.escribeLineaLog(hbl.LOGS_hblRedundancia, str(rst)) 

                # Si encuentra la unidad primaria llamada BOOTPRI y esta montada en /boot
                if rst[2] == 'vfat' and rst[4] == '/boot' and rst[5] == "BOOTPRI":                      
                    log.escribeLineaLog(hbl.LOGS_hblRedundancia, "Unidad primaria BOOTPRI en funcionamiento") 

                elif rst[2] == 'vfat' and rst[4] == '/boot' and rst[5] == "BOOTSEC": 
                    log.escribeLineaLog(hbl.LOGS_hblRedundancia, "Unidad secundaria BOOTSEC en funcionamiento") 

                elif rst[2] == 'vfat' and rst[4] == '/boot': 
                    log.escribeLineaLog(hbl.LOGS_hblRedundancia, "Unidad conectada en funcionamiento : " + rst[5])  
                

""" --------------------------------------------------------------------------------------------

    chequeo de la unidad en uso

-------------------------------------------------------------------------------------------- """

def leerRedundancia():

    # Separados en log
    log.escribeSeparador(hbl.LOGS_hblRedundancia)

    # Lee los nombres del volumen sda conectado, si ya tiene asignacion PRIMARIA / SECUNDARIA modifica
    # el flag para indicarlo al connect
    # si el nombre del volumen es otro, renombra a sda como PRIMARIA y al siguiente volumen vfat como secundaria

    # inicializo la variable
    Redundancia = 0
    
    # realiza un recorrido desde la primer letra hasta la ultima letra indicada en el json
    for x in range(ord(hbl.REDUNDANCIA_primeraLetraUnidad), ord(hbl.REDUNDANCIA_ultimaLetraUnidad) + 1):

        # realiza un recorrido por las particiones de cada unidad
        for i in range(int(hbl.REDUNDANCIA_primeraParticion), int(hbl.REDUNDANCIA_ultimaParticion) + 1):

            rst = hblCore.getVolumeNames("sd" + chr(x) + str(i)) 
            log.escribeLineaLog(hbl.LOGS_hblRedundancia, str(rst)) 
   
            if 'sda1' in str(rst) and rst[2] == 'vfat' and rst[4] == '/boot' and rst[5] == "BOOTPRI": 
                log.escribeLineaLog(hbl.LOGS_hblRedundancia, "> Unidad primaria activa") 
                Redundancia = 1 # queda redundancia disponible en la HBL

            elif 'sda1' in str(rst) and rst[2] == 'vfat' and rst[4] == '/boot' and rst[5] == "BOOTSEC":    
                log.escribeLineaLog(hbl.LOGS_hblRedundancia, "> Unidad secundaria activa") 
                Redundancia = 0 # NO queda redundancia disponible en la HBL, esta trabajando con la unidad Secundaria
        
    return Redundancia 
   

""" --------------------------------------------------------------------------------------------

    inicializacion chequeo de redundancia

-------------------------------------------------------------------------------------------- """

def inicializacion():  

    # chequeo si hay que renombrar las unidades por primera vez
    checkNombreVolumenes()

    # si funciona con la unidad secundaria, hay que hace un rescue de la primaria
    pass
 