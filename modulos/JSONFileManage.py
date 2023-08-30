import json

from modulos import log as log
from modulos import variablesGlobales as VG 
from modulos import hbl as hbl


class JSONFileManage(object):
    
    def __init__(self, file):
        self.file = file
    
    def getJSONFromFile(self):
        '''
            Devuelve Diccionario equivalente al JSON dentro del archivo
            en la ruta self.file
        '''
        VG.mutexBBDD_DNI_Patente.acquire()
        with open(self.file) as f:
            JSON = json.load(f)
            #print("JSON" + str(JSON))
        VG.mutexBBDD_DNI_Patente.release()
        return JSON
    
    def WriteJSONAsFile(self,newData):
        '''
            Escribe data en formato JSON dentro de un archivo
            con ruta self.file
        '''
        VG.mutexBBDD_DNI_Patente.acquire()
        
        with open(self.file, 'w') as convert_file:
            convert_file.write(json.dumps(newData,indent=6))
        VG.mutexBBDD_DNI_Patente.release()
            
    def add_Y_InFile(self,id,plate):
        '''
            Agrega una patente al id, en formato json.
            Devuelve diccionario actualizado con los cambios realizados.
            Sino Devuelve que salio mal
        '''
        try:
            #if str(plate) == "":
            #    errorStr = "ERROR: Patente VACIA"
            #    self.__LogReport(errorStr)
            #    return errorStr
            if str(id) == "":
                errorStr = "ERROR: DNI VACIO"
                self.__LogReport( errorStr)
                return errorStr
            
            JSON :dict = self.getJSONFromFile()
            patentes = JSON.get(str(id))
            
            if patentes is None:
                self.__LogReport( "Nuevo ID")
                JSON[str(id)] = [str(plate)]
            else:
                self.__LogReport( "ID ya existe")
                """Check si la patente no esta ya"""
                if str(plate) in patentes:
                    errorStr = "ERROR: Patente ya existe"
                    self.__LogReport( errorStr)
                    return errorStr
                else:
                    JSON[str(id)].append(str(plate))
                
            #print("newData" + str(JSON))
            self.WriteJSONAsFile(JSON)
            VG.newDataBBDD = True
            self.__LogReport( "BBDD actualizada")
            return "OK"
        
        except Exception as e:
            self.__LogReport( "Error al agregar data: " + str(e))
            return str(e)
    
    def remove_Y_InFile(self,id,plate):
        try:
            JSON : dict = self.getJSONFromFile()
            
            if JSON.get(str(id)) is None:
                errorStr = "El ID no existe"
                self.__LogReport( errorStr)
                return errorStr
            
            else:
                print("JSON" + str(JSON))
                if plate == "": # si no se especifica la patente, se borran todas
                    JSON.pop(str(id))
                else:
                    if str(plate) in JSON.get(str(id)): #Me fijo si la patente existe
                        JSON[str(id)].remove(str(plate)) #Borro la patente      
                    else:
                        errorStr = "La patente no existe"
                        self.__LogReport( errorStr)
                        return errorStr
                                     
                print("newData" + str(JSON))
                self.WriteJSONAsFile(JSON)
                VG.newDataBBDD = True
                self.__LogReport( "BBDD actualizada")
            
            return JSON
        except Exception as e:
            self.__LogReport( "Error al agregar data: " + str(e))
            return str(e)
        
    def __LogReport(self, mensaje):
        log.escribeSeparador(hbl.LOGS_FileManage)
        log.escribeLineaLog(hbl.LOGS_FileManage,mensaje)
       