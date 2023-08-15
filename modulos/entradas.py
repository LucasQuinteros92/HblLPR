
import pigpio
import datetime 

from modulos import log as log, variablesGlobales
from modulos import hbl as hbl
from modulos import cacheo as cacheo
 
""" --------------------------------------------------------------------------------------------


   Clase entradas hbl


-------------------------------------------------------------------------------------------- """

class Entradas: 

    def __init__(self, pi, in1, in2, callback):

        self.pi = pi
        self.in1 = in1
        self.in2 = in2

        self.callback = callback
 
        self.pi.set_mode(in1, pigpio.INPUT)
        self.pi.set_mode(in2, pigpio.INPUT) 
        
        self.in1 = self.pi.callback(in1, pigpio.FALLING_EDGE, self.callbackIN1)
        self.in2 = self.pi.callback(in2, pigpio.FALLING_EDGE, self.callbackIN2)  

    # ***************************************************************************************

    #   callback interrupcion entrada 1 HBL

    # ***************************************************************************************    
    
    def callbackIN1(self, gpio, level, tick): 

        diff = pigpio.tickDiff(variablesGlobales.pressTick, tick)

        log.escribeSeparador(hbl.LOGS_hblEntradas) 
        log.escribeLineaLog(hbl.LOGS_hblEntradas, "pressTick : " + str(variablesGlobales.pressTick)) 
        log.escribeLineaLog(hbl.LOGS_hblEntradas, "tick : " + str(tick)) 
        log.escribeLineaLog(hbl.LOGS_hblEntradas, "Diff : " + str(diff))  

        variablesGlobales.pressTick = tick

        if diff > hbl.DIG_in_pushDelay: 
            log.escribeSeparador(hbl.LOGS_hblEntradas)
            log.escribeLineaLog(hbl.LOGS_hblEntradas, hbl.DIG_in_in1_id) 

            # si esta activado el cacheo en esta HBL 
            # boton panico
            if hbl.CACHEO_activado == 1:
                cacheo.botonPanico(self.pi) 
    
    # ***************************************************************************************

    #   callback interrupcion entrada 2 HBL

    # ***************************************************************************************

    def callbackIN2(self, gpio, level, tick):  
 
        diff = pigpio.tickDiff(variablesGlobales.pressTick, tick)

        log.escribeSeparador(hbl.LOGS_hblEntradas) 
        log.escribeLineaLog(hbl.LOGS_hblEntradas, "pressTick : " + str(variablesGlobales.pressTick)) 
        log.escribeLineaLog(hbl.LOGS_hblEntradas, "tick : " + str(tick)) 
        log.escribeLineaLog(hbl.LOGS_hblEntradas, "Diff : " + str(diff)) 

        variablesGlobales.pressTick = tick

        if diff > hbl.DIG_in_pushDelay: 
            log.escribeSeparador(hbl.LOGS_hblEntradas)
            log.escribeLineaLog(hbl.LOGS_hblEntradas, hbl.DIG_in_in2_id) 
        
            # si esta activado el cacheo en esta HBL 
            # accionamiento de la activacion de la entrada 2
            if hbl.CACHEO_activado == 1:                
                cacheo.procesoCacheo(self.pi) 
 

    @staticmethod
    def readPin(pi, pin):
        valorPin = pi.read(pin)
        return valorPin

 