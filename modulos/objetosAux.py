import json

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