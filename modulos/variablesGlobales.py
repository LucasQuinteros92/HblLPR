
""" ******************************************************************************************

     variables globales  

****************************************************************************************** """ 
import threading
#
#   cacheo.py
#

global ubicacionCacheo  
global listaAleatoria
global valorEncontrado 
global cacheoActivo
  

#
#   hblCore.py
#  

global HBLCORE_contadorReset 


#
#   entradas.py
#  
  
global pressTick




# inicializacion variables globales
valorEncontrado = 0
ubicacionCacheo = 0 
cacheoActivo = 0
listaAleatoria = []
HBLCORE_contadorReset = 0
pressTick = 0

ultimaPatente = ""
listaPatentes = ["XXX114"] * 10
listaDNIs = []

lastDNI_Serial = "NULL"
mutexBBDD_DNI_Patente = threading.Lock()
mutexReporte_DNI_Patente = threading.Lock()
newDataBBDD = True

