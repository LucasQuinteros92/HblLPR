import threading as Thread
import modulos.variablesGlobales as VG
import requests
import datetime
import modulos.hbl as hbl
import modulos.log as log
import json
import os

dataSimple = 0 # Un request sin parametros
dataData = 1 # Un request con data como parametro
dataJSON = 2 # Un request con un json como parametro

modoSincronico = 0
modoAsincronico = 1

semaforoRequest = Thread.Lock()

url = "https://visitas-dev.jphlions.com/api/visitas/custom/evento_visita"

payload = json.dumps({
  "Event": {
    "id": "123456",
    "plate": "AAA000"
  }
})
headers = {
  'Authorization': 'Basic bGlvbnM6SnBoMTM1',
  'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImlkIjo0LCJuYW1lIjoiYWRtaW4iLCJzdXJuYW1lIjoibml0cm80IiwiZW1haWwiOiJuaXRybzRAanBobGlvbnMuY29tIiwicHJvdmlkZXIiOiJsb2NhbCIsImFwcGxpY2F0aW9uSWQiOjN9LCJjbGllbnRJZCI6ImpiODQ5ZDQ4M2I4NzIiLCJleHBpcmUiOiIyMDIzLTA1LTA3VDE1OjA4OjA4LjQ2MloiLCJpYXQiOjE2ODIwODk2ODgsInZlbmNpbWllbnRvIjoxNjgzNDcyMDg4NDYyLCJ2ZW5jaW1pZW50b190ZXN0IjoxNjgzNDcyMDg4NDYyLCJpZCI6NCwiZGF0b3NDb25leGlvbiI6eyJtb3Rvcl9kYiI6Im1zc3FsIiwiaG9zdF9kYiI6IjAyLmRldi5qcGhsaW9ucy5jb20iLCJwb3J0X2RiIjoiMTQzMyIsIm5hbWVfZGIiOiJWSVNJVEFTIiwidXNlcl9kYiI6InNhIiwicGFzc19kYiI6IkpwaExpb25zMTM1I0RldiJ9LCJpZFVzdWFyaW9OaXRybzQiOjQsInVzdWFyaW8iOiJhZG1pbiBuaXRybzQifQ.p0NtfxxLwUpD_ZVzdT1-jFwMflWYD3H-8d8txhWi6YE',
  'Content-Type': 'application/json'
}


class requestnblck(object):
    def __init__(self,modo ,dataType = dataSimple, data = None, file = None ) -> None:
        if hbl.REQ_activado == 1:
            self.__running = False
            self.data = data
            self.file = file
            self.modo = modo  # Sincronico o asisncrionico
            self.dataType = dataType #Tipo de dato que se va a enviar como parametro en el request
            self.lastRequest = datetime.datetime.now()
            
            if hbl.REQ_seleccionURL == 1:
                self.UrlCompletaReq = hbl.REQ_urlRequest1
            elif hbl.REQ_seleccionURL == 2:
                self.UrlCompletaReq = hbl.REQ_urlRequest2
            elif hbl.REQ_seleccionURL == 3:
                self.UrlCompletaReq = hbl.REQ_urlRequest3
            elif hbl.REQ_seleccionURL == 4:
                self.UrlCompletaReq = hbl.REQ_urlRequest4
            elif hbl.REQ_seleccionURL == 5:
                self.UrlCompletaReq = hbl.REQ_urlRequest5
            else:
                self.UrlCompletaReq = "http://www.google.com"
            
            
            self.t = Thread.Thread(target=self.__run, daemon=False)
            
    def is_running(self):
        return self.__running
    
    def start(self):
        self.__running = True
        self.t.start()
        
    def pause(self):
        self.is_running = False
        
    def request(self,data,url=None):
        if url != None:
            self.UrlCompletaReq = url
        self.data = data
        semaforoRequest.release()
        
        
    def requestJSONFile(self,file = None,url=None):
        try:
            if url != None:
                self.UrlCompletaReq = url
            if file != None:
                self.file = file
            
            
            VG.mutexReporte_DNI_Patente.acquire()
            with open('data.json') as json_file:
                json_data = json.load(json_file)   
            VG.mutexReporte_DNI_Patente.acquire() 
                
            self.dataType = dataJSON
            self.data = json_data
            semaforoRequest.release()
            
        except Exception as e:
            self.__Logreport("Error al intentar hacer req: "+ str(e))
            
    
    def getJSONfromFIle(self):
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
                
                os.remove(hbl.Validacion_Doble_Factor_reportFile)
                
            else:
                return "NULL"
                
        except Exception as e:
            print(e)
        return json_data
        
        
    
    def __run(self):
        while True:
            if self.modo == modoAsincronico:
                semaforoRequest.acquire()
            else:
                semaforoRequest.acquire(timeout=hbl.Validacion_Doble_Factor_periodReport)
                
            try:
                if self.dataType == dataSimple:
                    req = requests.get(self.UrlCompletaReq, 
                                       timeout=int(hbl.REQ_timeoutRequest))
                elif self.dataType == dataJSON:
                    self.data = self.getJSONfromFIle()
                    #req = requests.post(self.UrlCompletaReq, json=self.data,timeout=int(hbl.REQ_timeoutRequest))
                    if self.data!="NULL":
                        req = requests.request("POST", url, headers=headers,data=json.dumps(self.data))
                        self.__Logreport(req.text)
                self.__Logreport("request exitoso:"+ str(self.UrlCompletaReq) +str(req) )
                
            except Exception as e:
                self.__Logreport("Error al intentar hacer req: "+ str(e))
                    
                
    def __Logreport(self,texto):
        log.escribeSeparador(hbl.LOGS_hblRequest)
        log.escribeLineaLog(hbl.LOGS_hblRequest,texto)