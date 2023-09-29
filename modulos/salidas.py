import pigpio
 
from modulos import hbl as hbl
from modulos import delays as delays
from modulos import log as log
import threading as Thread
import queue

""" --------------------------------------------------------------------------------------------

   Clase salidas hbl
   
-------------------------------------------------------------------------------------------- """
q = queue.Queue()

class Salidas:

    def __init__(self, pi):

        self.pi = pi 
        self.__stop = True
        #self.pi.write(hbl.DIG_out_pin_out1, hbl.OFF)   
        self.pi.write(hbl.DIG_out_pin_out2, hbl.ON) 
        self.pi.write(hbl.DIG_out_pin_out3, hbl.OFF) 
        self.pi.write(hbl.DIG_out_pin_out4, hbl.OFF)

        # si el port0 de wiegand esta desactivado, puedo usar los
        # pines como salidas digitales, las inicializo

        if hbl.WD_port0_activado == 0:

            self.pi.write(hbl.DIG_out_pin_out5, hbl.OFF)   
            self.pi.write(hbl.DIG_out_pin_out6, hbl.OFF) 
            self.pi.write(hbl.DIG_out_pin_out7, hbl.OFF) 
            self.pi.write(hbl.DIG_out_pin_out8, hbl.OFF)
        
        self.t = Thread.Thread(target=self.__run, daemon=False,  name="Salidas")
        self.t.start()
        log.escribeSeparador(hbl.LOGS_Salidas) 
        log.escribeLineaLog(hbl.LOGS_Salidas,"Salidas Inicializadas") 
    

    def activaSalida(self, pin, tiempo):
        q.put({"pin":pin,"tiempo":tiempo})
        log.escribeSeparador(hbl.LOGS_Salidas) 
        log.escribeLineaLog(hbl.LOGS_Salidas,f"Salidas {pin} activada por {tiempo}") 
        
    def cambioEstadoSalida(self, pi, pin, estado): 
        self.pi.write(pin, estado)
    
    def stop(self):
        self.__stop = False
        log.escribeSeparador(hbl.LOGS_Salidas) 
        log.escribeLineaLog(hbl.LOGS_Salidas,f"MODULO SALIDA DETENIDO")
        
    def __run(self):
        while self.__stop:
            try:
                data = q.get(timeout=5)
                self.pi.write(data["pin"], hbl.OFF) 
                delays.ms(int(data["tiempo"]))
                self.pi.write(data["pin"], hbl.ON)  
                q.task_done()
            except:
                pass