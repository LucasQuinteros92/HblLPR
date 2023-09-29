from threading import Thread
import time


from modulos import auxiliar as auxiliar
from modulos import hbl as hbl
from datetime import datetime
from modulos import variablesGlobales as VG
from modulos import log as log
from modulos import salidas as salidas
from modulos import JSONFileManage as JSONFileManage
from modulos import WebSocket as WebSocket
from modulos import objetosAux as obAux
import json
import os


ID_ANY_PATENTE = "?"
FACTOR_DOBLE  = 2
FACTOR_SIMPLE = 1

payload = json.dumps({
    "nuevaVisita": {
    "id": "123456",
    "dominio": "AAA000"
    },
    "msjID" : "1685727490"
    
})

class Validacion_Doble_Factor(object):

    def __init__(self, objWebSock, pi):
        self.newDNI = "NULL"
        self.patentes_esperadas = []
        self.patentes_LPR = []
        self.pi = pi
        self.BBDD :dict  = {}
        self.lastDNI_reportado = ""
        self.doble_factor_activado = True
        self.objWebSock : WebSocket.WebSocket = objWebSock
        self.JSONFILEBBDD = hbl.Validacion_Doble_Factor_JSONBBDDPATH
        self.BDJSON = JSONFileManage.JSONFileManage(self.JSONFILEBBDD)
        self.__stop = True
        #self.objWebSock.ws.on_message = self.nuevoEventoRecibido
        #self.nuevoEventoRecibido(payload)
        self.__LogReport("LPR STARTED")
        if hbl.Validacion_Doble_Factor_activado == 1:
            self.t = Thread(target = self.__run, daemon= False,name="DobleFactor")
            self.t.start()
    
    def nuevoEventoRecibido(self,ws, message):
        mensajeDict : dict= json.loads(message)
        keys = list(mensajeDict.keys())
        data :dict = json.loads(mensajeDict.get(keys[1]) )
        evento :str   = data.get("evento")
        msgId  :str   = data.get("msgId")
        datos  :dict  = data.get("datos")
        res = ""
        self.objWebSock.on_message(None,message)
        
        if evento == "nuevaVisita":
            #add : dict = evento.get("nuevaVisita")
            #self.agregar_Y_(add.get("id"),add.get("plate"))
            res = self.BDJSON.add_Y_InFile(datos.get("Persona"),datos.get("Wiegand"),datos.get("Vehiculo"))
           
        elif evento ==  "remove":
            #remove :dict = datos.get("remove")
            res = self.BDJSON.remove_Y_InFile(datos.get("Persona"),datos.get("Vehiculo"))
        
        elif evento == "actualizacionConfig":
            #config : dict = evento.get("actualizacionConfig")
            if datos.get("Nombre") == "DOBLE_FACTOR_VALIDACION":
                res = self.cambiarFactor(datos.get('Valor'))
            else:
                res= "ConfiguracionDesconocida"
    
        eventoRes = self.generarEventoRespuesta(data,msgId)
    
        self.enviar_AlServerSiEstaConectado(eventoRes)
        
    def generarEventoRespuesta(self,data : dict ,msgId):
        
        evento = json.dumps({
            "evento": "",
            "datos" : {
                "clientId" : hbl.WebSocket_ClientId,
                "msgId": msgId,
                "data": data,
                "status": 1
                },
            "msgId" : msgId
        })
        
        return evento

    def generarEventoReporte(self,evento,DNI="",patente = ""):
        now = datetime.now()
        date = datetime.timestamp(now)
        evento = json.dumps({
            "evento" : evento,
            "datos" : {
                "Persona": DNI,
                "Vehiculo" : patente,
                "fechaHora": date,
                "clientId": hbl.WebSocket_ClientId,
                "clientName" : hbl.WebSocket_ClientName
            },
            "msgId" : date
        })

        return evento
    
    def enviar_AlServerSiEstaConectado(self, evento):
        #respuesta:{"borrarMsj":"1685727490", "clientId":"NOMBRE O ID HBL"}
        
        if self.objWebSock.estaConectado():
            res = self.objWebSock.send_message(evento)
            self.siHayPendientesEnviarAlServer()

        else:
            self.guardarEvento(evento)
            res = False
            
        return res
    
    def siHayPendientesEnviarAlServer(self):
        if self.hayPendientes():
            eventosPendientes = self.recuperarPendientes() 
            for evento in eventosPendientes:
                self.objWebSock.send_message(str(evento))
                time.sleep(0.1)
            self.eliminarPendientes()
            #print("enviando pendientes")

    def hayPendientes(self):
        return os.path.exists(hbl.Validacion_Doble_Factor_reportFile)
    
    def eliminarPendientes(self):
        os.remove(hbl.Validacion_Doble_Factor_reportFile) 

    def cambiarFactor(self,valor : bool):
    
        self.doble_factor_activado = valor
        res = "FACTOR_ACTUALIZADO"
        return res
        
    def __run(self):
        while self.__stop:
            """Ver como gestionar la lectura de dni. Voy a leer el dni cada x tiempo
            pero ¿voy a tomar solo el ultimo dni o voy a leer los dnis que ficharon en
            ese intervalo de tiempo?"""
            #print("dob")
            if self.objWebSock.reconnected:
                
                self.objWebSock.reconnected = False
                self.objWebSock.ws.on_message = self.nuevoEventoRecibido
                self.siHayPendientesEnviarAlServer()
                
            if self.seDetectoPatente():
                    self.reportarDeteccion(self.seDetectoPatente())
                    self.borrarPatenteDetectada()
                
            self.newDNI = self.get_dni()
             
            if self.newDNI != "NULL":
                
                self.actualizaBBDDSiHayDataNueva()
                
                self.AccesoSegunFactoresYReportar()
                
                self.resetNewDNI()
            
            time.sleep(1)
    
    def stop(self):
        self.__stop = False
        self.__LogReport("LPR STOPPED")
            
    def AccesoSegunFactoresYReportar(self):
        '''
            Si esta activado el doble factor verificara ambos factores,
            sino verificara simple factor solamente
        '''
        
        if self.factorDobleActivado(): 
            self.PermitirAccesoSiCumpleYReportar(self.cumpleFactorSimple(),
                                                 self.cumpleFactorDoble())      
        
        else:
            self.PermitirAccesoSiCumpleYReportar(self.cumpleFactorSimple())
    
    def PermitirAccesoSiCumpleYReportar(self,factorSimple,factorDoble = True):   
        '''
            Permitira el acceso si se cumplen ambos factores
            sino reportara cual fue el primer factor en no cumplirse
        '''
        if factorSimple and factorDoble:
        
            self.PermitirAcceso()
            self.reportarAccesoSegunFactores()
            
        elif not factorSimple:
            self.__LogReport("DNI DESCONOCIDO: " +self.newDNI)
            
        elif factorSimple and not factorDoble:
            patentes = ""
            for patente in self.patentes_esperadas:
                patentes += "\n" + patente
            self.__LogReport("PATENTES NO ENCONTRADAS: " + patentes)
            
    def reportarAccesoSegunFactores(self):
        '''
            Reporta en log y al server a quien se le otorgo el acceso
        '''
        if self.factorDobleActivado():
            patente = self.validar_patente()
            self.__LogReport(patente, FACTOR_DOBLE)
            self.siElDniEsNuevoReportar(patente)
            
        else:
            self.__LogReport("-", FACTOR_SIMPLE)
            self.siElDniEsNuevoReportar("-")

    def PermitirAcceso(self):
        
        self.abrir_barrera()
        
    def factorDobleActivado(self):
        
        return self.doble_factor_activado
    
    def cumpleFactorSimple(self):
        
        if self.dniValido():
            cumple = True
        else:
            cumple = False

        return cumple
        
    def cumpleFactorDoble(self):

        if self.esUnaPatenteValida():
            Cumple = True
        else:
            Cumple = False
        
        return Cumple
    
    def actualizaBBDDSiHayDataNueva(self):
        '''
            actualiza la base de datos local(archivo json)
            si hay un dato nuevo en la misma 
            sino no hace nada
        '''
        try:
            if VG.newDataBBDD:
                VG.mutexBBDD_DNI_Patente.acquire()
                with open('/usr/programas/hbl/modulos/BBDD_RUT_Patente.json') as f:
                    self.BBDD = json.load(f)
                    #print(data)
                VG.mutexBBDD_DNI_Patente.release()
                VG.newDataBBDD = False
        except Exception as e:
            print(str(e))
            lista = []
            return lista #Checkear esto
    
    def abrir_barrera(self):
        """Esta bien abrir la barrera asi ?"""
        salidas.Salidas(self.pi).activaSalida(pin=hbl.DIG_out_pin_out2,tiempo=3000)
    
    def seDetectoPatente(self):
        return VG.ultimaPatente
    
    def borrarPatenteDetectada(self):
        VG.ultimaPatente = ""
        
    def get_patentes_from_LPR(self):
        '''
        devuelve las ultimas 10 patentes capturadas por la camara
        '''
        return VG.listaPatentes
        
    def reportarDeteccion(self,patente):
        
        eventoNuevaDeteccion = self.generarEventoReporte("nuevaPatente",patente=patente)
        self.reportar(eventoNuevaDeteccion)
    
    def siElDniEsNuevoReportar(self,patente):
        
        #if self.lastDNI_reportado != self.newDNI:
            
        self.lastDNI_reportado = self.newDNI
        now = datetime.now()
        #.strftime('%Y-%m-%d %H:%M:%S')
        #evento = {"RUT":self.newDNI, "Patente":patente, "FechaHora":datetime.timestamp(now),"id":hbl.HblID}
        
        eventoEntrada = self.generarEventoReporte("nuevoIngreso",self.newDNI,patente)
        self.reportar(eventoEntrada)
        #else:
        #    self.__LogReport("DNI ya reportado")
            
    def reportar(self,evento):
            self.enviar_AlServerSiEstaConectado(evento)

    def guardarEvento(self, evento):
            try:
                VG.mutexReporte_DNI_Patente.acquire()
                if os.path.isfile(hbl.Validacion_Doble_Factor_reportFile):
                    jsonFile = open(hbl.Validacion_Doble_Factor_reportFile, "a")
                    jsonFile.write("," + evento)
                    jsonFile.close()
                else:
                    jsonFile = open(hbl.Validacion_Doble_Factor_reportFile, "w")
                    jsonFile.write(evento)
                    jsonFile.close()
                VG.mutexReporte_DNI_Patente.release()
            except Exception as e:
                print(e)

    def recuperarPendientes(self):
        try:
            if os.path.isfile(hbl.Validacion_Doble_Factor_reportFile):
                """Posicionarse al principo, agregar '[' y posicionarse al final, borrar la coma y escribir ']'"""
                """jsonFile = open(hbl.Validacion_Doble_Factor_reportFile, "a")
                jsonFile.write("]")
                jsonFile.close()"""
            
                with open(hbl.Validacion_Doble_Factor_reportFile) as json_file:
                    json_data = json_file.read()
                    json_data = "[" + json_data + "]"
                    json_data = json.loads(json_data)
                    #json_data = json.load(json_file) 
                    #json_data = "{" + json_data + "}"
                
                #os.remove(hbl.Validacion_Doble_Factor_reportFile)
                
            else:
                return "NULL"
                
        except Exception as e:
            print(e)
        return json_data

    def resetNewDNI(self):
        VG.lastDNI_Serial = "NULL"
        
    def get_dni(self):
        '''
            devuelve dni asociado al wiegand leido por la ras
        '''
        
        return self.BDJSON.getDNIfromWD(VG.lastDNI_Serial)

    def validar_patente(self):
        '''
            Devuelve la primer patente esperada asociada al dni
            si la encuentra en las ultimas 10 patentes captadas por la camara
            sino devuelve NO_MATCH
        '''
        try:
            self.patentes_esperadas = self.get_patentes_asociadas_from_BBDD()
            self.patentes_LPR = self.get_patentes_from_LPR()
            
            if "?" in self.patentes_esperadas:
                return "?"
            
            for p in self.patentes_esperadas:
                if p in self.patentes_LPR:
                    return p
            
            
            return "NO MATCH"
        except Exception as e:
            return "NO MATCH"
         
    def dniValido(self):
        '''
            indica si el dni existe en la base de dato
            retorna booleano
        '''
        
        for p in self.BBDD.keys():
            if self.newDNI == p:
                return True
        
        return False
    
    def esUnaPatenteValida(self):
        if self.dniValido() and self.validar_patente() != 'NO MATCH':
            
            return True
        else:
            
            return False
              
    def get_patentes_asociadas_from_BBDD(self):
        '''
           devuelve las patentes asociadas al dni en la base de datos
        '''    
        return self.BBDD[self.newDNI]["patentes"]
                    
    def __LogReport(self,data ,factor = None):
        log.escribeSeparador(hbl.LOGS_hblDobleFactor) 
        if factor == FACTOR_DOBLE:
            log.escribeLineaLog(hbl.LOGS_hblDobleFactor, "FACTOR DOBLE")
            log.escribeLineaLog(hbl.LOGS_hblDobleFactor, "DNI : " + str(self.newDNI))
            log.escribeLineaLog(hbl.LOGS_hblDobleFactor, "Patentes esperadas : " + str(self.patentes_esperadas))
            log.escribeLineaLog(hbl.LOGS_hblDobleFactor, "Ultima patentes : " + str(self.patentes_LPR))
            log.escribeLineaLog(hbl.LOGS_hblDobleFactor, "Patente '" + str(data) + "' validada")
        elif factor == FACTOR_SIMPLE:
            log.escribeLineaLog(hbl.LOGS_hblDobleFactor, "FACTOR SIMPLE")
            log.escribeLineaLog(hbl.LOGS_hblDobleFactor, "DNI VALIDADO: " + str(data))
        else:
            log.escribeLineaLog(hbl.LOGS_hblDobleFactor, str(data))
            
    """def borrar_y_SiExisten(self,dni,patentes):
        '''
            Borrara dni y usuario si existen en la base de datos local
        '''
        print(dni, patentes)
        if dni != None and patentes != None:
            self.borrar_Del_(patentes,dni)
            
        elif patentes == None:
            self.borrar_(dni)
            
    def borrar_Del_(self,patentes, dni):
        print("borrar patente")
            
    def borrar_(self,dni):
        print("borrar usuario")
        
    def agregar_Y_(self,dni,patente):
        pass"""