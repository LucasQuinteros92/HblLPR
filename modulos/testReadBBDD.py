import json
def get_patente_from_BBDD(newDNI):
    try:
        with open('/usr/programas/hbl/modulos/BBDD_RUT_Patente.json') as f:
            data = json.load(f)
            #print(data)
        return data[newDNI]
    except Exception as e:
        lista = []
        return lista #Checkear esto

def validar_patente(patentes_esperadas,lst):
    for x in patentes_esperadas:
        for y in lst:
            if x == y:
                return x
    return "NO MATCH"
            
def reportar(patente):
    try:
        evento = {"RUT":"40951294", "Patente":patente}
        jsonString = json.dumps(evento)
        jsonFile = open("data.json", "a")
        jsonFile.write(jsonString + "\n")
        jsonFile.close()
    except Exception as e:
        print("No se pudo hacer el reporte")
        
        
lst = ["NULL"] * 10


for x in range(0,15):
    lst.append(lst.pop(0)) 
    lst[len(lst)-1] = str(x)
    
print(lst)

patente_validada = validar_patente(["5","53"],lst=lst)
print(patente_validada)

reportar(patente_validada)
            
"""print(get_patente_from_BBDD("40951294"))
print(get_patente_from_BBDD("41356847")[0])
print(get_patente_from_BBDD("41356847")[1])"""




    
    