import os
import sys
import time
import random

from modulos import hbl as hbl
from modulos import variablesGlobales as variablesGlobales
from modulos import log as log


""" ******************************************************************************************

    PINOUT 

        luzVerde = DIG_out_pin_out1
        sirena  = DIG_out_pin_out2
        luzRoja = DIG_out_pin_out3
        barrera = DIG_out_pin_out4

****************************************************************************************** """  


def aleatorioValor(cacheosPositivos, cantidadCacheos):

    try:

        random.seed()
        listaNumeros = random.sample(range(0, cantidadCacheos), cacheosPositivos) 
        listaNumeros.sort()

        return listaNumeros
    
    except Exception as e:  

        exc_type, exc_obj, exc_tb = sys.exc_info() 
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
        errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

        log.escribeSeparador(hbl.LOGS_hblCacheo)
        log.escribeLineaLog(hbl.LOGS_hblCacheo, "Error : " + str(errorExcepcion))

""" ******************************************************************************************

     



****************************************************************************************** """ 

def ApagaReles(pi):

    try:

        pi.write(hbl.DIG_out_pin_out1, hbl.OFF)    
        pi.write(hbl.DIG_out_pin_out2, hbl.OFF)
        pi.write(hbl.DIG_out_pin_out3, hbl.OFF)
        pi.write(hbl.DIG_out_pin_out4, hbl.OFF)

    except Exception as e:  

        exc_type, exc_obj, exc_tb = sys.exc_info() 
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
        errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

        log.escribeSeparador(hbl.LOGS_hblCacheo)
        log.escribeLineaLog(hbl.LOGS_hblCacheo, "Error : " + str(errorExcepcion))

""" ******************************************************************************************

     

     

****************************************************************************************** """ 

def AbreBarrera(pi):
   
    try:

        pi.write(hbl.DIG_out_pin_out4, hbl.ON)
    
    except Exception as e:  

        exc_type, exc_obj, exc_tb = sys.exc_info() 
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
        errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

        log.escribeSeparador(hbl.LOGS_hblCacheo)
        log.escribeLineaLog(hbl.LOGS_hblCacheo, "Error : " + str(errorExcepcion))  

""" ******************************************************************************************

     

     

****************************************************************************************** """ 

def CierraBarrera(pi):

    try:

        pi.write(hbl.DIG_out_pin_out4, hbl.OFF)

    except Exception as e:  

        exc_type, exc_obj, exc_tb = sys.exc_info() 
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
        errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

        log.escribeSeparador(hbl.LOGS_hblCacheo)
        log.escribeLineaLog(hbl.LOGS_hblCacheo, "Error : " + str(errorExcepcion))  
   
""" ******************************************************************************************

     

     

****************************************************************************************** """ 

def NoPasa(pi):

    try: 

        contador = 0

        while contador < hbl.CACHEO_repRelePositivo:
            pi.write(hbl.DIG_out_pin_out2, hbl.ON)
            pi.write(hbl.DIG_out_pin_out3, hbl.ON)
            time.sleep(int(hbl.CACHEO_tiempoRelePositivo))
            pi.write(hbl.DIG_out_pin_out2, hbl.OFF)
            pi.write(hbl.DIG_out_pin_out3, hbl.OFF)
            time.sleep(int(hbl.CACHEO_tiempoRelePositivo))
            contador = contador + 1
        
        # abre la barrera
        AbreBarrera(pi)
        time.sleep(int(hbl.CACHEO_tiempoRelePositivo))    
        # cierra la barrera
        CierraBarrera(pi)  

    except Exception as e:  

        exc_type, exc_obj, exc_tb = sys.exc_info() 
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
        errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

        log.escribeSeparador(hbl.LOGS_hblCacheo)
        log.escribeLineaLog(hbl.LOGS_hblCacheo, "Error : " + str(errorExcepcion))

""" ******************************************************************************************

     

     

****************************************************************************************** """ 

def Pasa(pi):

    try:

        contador = 0

        # abre la barrera
        AbreBarrera(pi)
        time.sleep(int(hbl.CACHEO_tiempoReleNegativo))  
        # cierra la barrera
        CierraBarrera(pi)  

        while contador < hbl.CACHEO_repReleNegativo:
            pi.write(hbl.DIG_out_pin_out1, hbl.ON)
            time.sleep(int(hbl.CACHEO_tiempoReleNegativo))
            pi.write(hbl.DIG_out_pin_out1, hbl.OFF)
            time.sleep(int(hbl.CACHEO_tiempoReleNegativo))
            contador = contador + 1
    
    except Exception as e:  

        exc_type, exc_obj, exc_tb = sys.exc_info() 
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
        errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

        log.escribeSeparador(hbl.LOGS_hblCacheo)
        log.escribeLineaLog(hbl.LOGS_hblCacheo, "Error : " + str(errorExcepcion))

""" ******************************************************************************************

     

     

****************************************************************************************** """ 

def botonPanico(pi):

    try:
 
        log.escribeLineaLog(hbl.LOGS_hblCacheo, "NoPasa (Boton Panico Activado)")
        NoPasa(pi) 
    
    except Exception as e:  

        exc_type, exc_obj, exc_tb = sys.exc_info() 
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
        errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

        log.escribeSeparador(hbl.LOGS_hblCacheo)
        log.escribeLineaLog(hbl.LOGS_hblCacheo, "Error : " + str(errorExcepcion)) 

""" ******************************************************************************************

     

     

****************************************************************************************** """ 

def procesoCacheo(pi):

    try:
        
        if variablesGlobales.ubicacionCacheo >= hbl.CACHEO_cantidadCacheos:
            variablesGlobales.ubicacionCacheo = 0

        # si el valor de ubicacionCacheo es 0, significa que recien empieza el cacheo entonces
        # calcula las n posiciones a cachear por positivo
        if variablesGlobales.ubicacionCacheo == 0:           

            variablesGlobales.listaAleatoria = aleatorioValor(hbl.CACHEO_cacheosPositivos, hbl.CACHEO_cantidadCacheos)       

            log.escribeSeparador(hbl.LOGS_hblCacheo)       
            log.escribeLineaLog(hbl.LOGS_hblCacheo, "Calculo de valores de posicion de cacheo : " + str(variablesGlobales.listaAleatoria)) 
            log.escribeLineaLog(hbl.LOGS_hblCacheo, "Cantidad de cacheos : " + str(hbl.CACHEO_cantidadCacheos)) 
            log.escribeLineaLog(hbl.LOGS_hblCacheo, "Cantidad de cacheos positivos: " + str(hbl.CACHEO_cacheosPositivos)) 
 
        for n in variablesGlobales.listaAleatoria:
             
            if variablesGlobales.ubicacionCacheo == n:   
                variablesGlobales.valorEncontrado = 1

        if variablesGlobales.valorEncontrado == 1:
            NoPasa(pi)
            log.escribeLineaLog(hbl.LOGS_hblCacheo, "NoPasa :" + str(variablesGlobales.ubicacionCacheo)) 
        else:
            Pasa(pi)
            log.escribeLineaLog(hbl.LOGS_hblCacheo, "Pasa :" + str(variablesGlobales.ubicacionCacheo))            
         
        # incrementa la variable en 1
        variablesGlobales.ubicacionCacheo = variablesGlobales.ubicacionCacheo + 1
        # reinicia la variable 
        variablesGlobales.valorEncontrado = 0 
    
    except Exception as e:  

        exc_type, exc_obj, exc_tb = sys.exc_info() 
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] 
        errorExcepcion = "ERROR - archivo : " + str(fname) + " - linea : " + str(sys.exc_info()[-1].tb_lineno) + " - mensaje : " + str(exc_obj) 

        log.escribeSeparador(hbl.LOGS_hblCacheo)
        log.escribeLineaLog(hbl.LOGS_hblCacheo, "Error : " + str(errorExcepcion))  