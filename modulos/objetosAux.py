import json
from datetime import datetime
from modulos import hbl as hbl

class Persona():
    '''
    Define una una person con
    dni 
    wiegand 
    patentes (lista opcional)
    '''
    
    def __init__(self, dni : str, wiegand : str ,patentes = []) -> None:
        self._dni       = dni.__str__()
        self._wiegand   = wiegand.__str__()
        if patentes == "":
            self._patentes  = []
        else:
            self._patentes = patentes
        
    def dictFormat(self):
        personaDict = {
            self._dni : {
                "wiegand" : self._wiegand,
                "patentes": self._patentes
            } 
            
        } 
        
        return personaDict
        
    def jsonFormat(self):
        
        personaJson = json.dumps(self.dictFormat()) 
        
        return personaJson
    
class Evento():
    def __init__(self, evento, dni =None, wiegand=None, patente=None,data = None,msgId = None) -> None:
        self._nombre  = evento
        self._dni     = dni
        self._wiegand = wiegand
        self._patente = patente
        self._data    = data
        self._msgId   = msgId
        
        
class EventoReporte(Evento):
    def __init__(self,nombre, dni, patente= ""):
        super().__init__(evento=nombre, dni=dni, patente=patente)
        now = datetime.now()
        date = datetime.timestamp(now)
        self._json = json.dumps({
            "evento" : self._nombre,
            "datos" : {
                "Persona": self._dni,
                "Vehiculo" : self._patente, 
                "fechaHora": date,
                "clientId": hbl.WebSocket_ClientId,
                "clientName" : hbl.WebSocket_ClientName
            },
            "msgId" : date
        })
        
class EventoRespuesta(Evento):
    def __init__(self, data, msgId) -> None:
        super().__init__(evento="RESPUESTAMSJ", data=data, msgId=msgId)
        
        self._json = json.dumps({
            "evento": self._nombre,
            "datos" : {
                "clientId" : hbl.WebSocket_ClientId,
                "msgId": msgId,
                "data": data,
                "status": 1
                },
            "msgId" : msgId
        })