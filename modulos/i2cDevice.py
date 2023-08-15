import pigpio
 
from modulos import lcd_i2c as lcd_i2c
from modulos import hbl as hbl
from modulos import delays as delays
from modulos import log as log


global lcd1
global lcd2
global lcd3
global lcd4

def inicializacion(pi):

    global lcd1
    global lcd2
    global lcd3
    global lcd4

    # inicializa displays LCD   
    try:
        if hbl.DISPLAY_display1_activado == 1:
            lcd1 = lcd_i2c.lcd(pi, width=int(hbl.DISPLAY_display1_width), addr=int(hbl.DISPLAY_display1_address,0)) 
            delays.ms(100)
            # lcd1.put_line(0, "HBL")  
            # lcd1.put_line(3, hbl.DISPLAY_display1_address)  
 
    except Exception as inst: 

        log.escribeSeparador(hbl.LOGS_hbli2c) 
        log.escribeLineaLog(hbl.LOGS_hbli2c, "Error display addr : " + hbl.DISPLAY_display1_address)
        log.escribeLineaLog(hbl.LOGS_hbli2c, "Error : " + str(inst))
    
    try:
        if hbl.DISPLAY_display2_activado == 1:
            lcd2 = lcd_i2c.lcd(pi, width=int(hbl.DISPLAY_display2_width), addr=int(hbl.DISPLAY_display2_address,0)) 
            delays.ms(100)
            # lcd2.put_line(0, "HBL")  
            # lcd2.put_line(3, hbl.DISPLAY_display2_address)  
    
    except Exception as inst: 

        log.escribeSeparador(hbl.LOGS_hbli2c) 
        log.escribeLineaLog(hbl.LOGS_hbli2c, "Error display addr : " + hbl.DISPLAY_display2_address)
        log.escribeLineaLog(hbl.LOGS_hbli2c, "Error : " + str(inst))

    try:
        if hbl.DISPLAY_display3_activado == 1:
            lcd3 = lcd_i2c.lcd(pi, width=int(hbl.DISPLAY_display3_width), addr=int(hbl.DISPLAY_display3_address,0)) 
            delays.ms(100)
            lcd3.put_line(0, "HBL")  
            lcd3.put_line(3, hbl.DISPLAY_display3_address) 

    except Exception as inst: 

        log.escribeSeparador(hbl.LOGS_hbli2c) 
        log.escribeLineaLog(hbl.LOGS_hbli2c, "Error display addr : " + hbl.DISPLAY_display3_address)
        log.escribeLineaLog(hbl.LOGS_hbli2c, "Error : " + str(inst))
            
    try:
        if hbl.DISPLAY_display4_activado == 1:
            lcd4 = lcd_i2c.lcd(pi, width=int(hbl.DISPLAY_display4_width), addr=int(hbl.DISPLAY_display4_address,0))
            delays.ms(100) 
            lcd4.put_line(0, "HBL")  
            lcd4.put_line(3, hbl.DISPLAY_display4_address) 

    except Exception as inst: 

        log.escribeSeparador(hbl.LOGS_hbli2c) 
        log.escribeLineaLog(hbl.LOGS_hbli2c, "Error display addr : " + hbl.DISPLAY_display4_address)
        log.escribeLineaLog(hbl.LOGS_hbli2c, "Error : " + str(inst))

    try:
        if hbl.DISPLAY_display5_activado == 1:
            lcd4 = lcd_i2c.lcd(pi, width=int(hbl.DISPLAY_display5_width), addr=int(hbl.DISPLAY_display5_address,0))
            delays.ms(100) 
            lcd4.put_line(0, "HBL")  
            lcd4.put_line(3, hbl.DISPLAY_display5_address) 

    except Exception as inst: 

        log.escribeSeparador(hbl.LOGS_hbli2c) 
        log.escribeLineaLog(hbl.LOGS_hbli2c, "Error display addr : " + hbl.DISPLAY_display5_address)
        log.escribeLineaLog(hbl.LOGS_hbli2c, "Error : " + str(inst))

    try:
        if hbl.DISPLAY_display6_activado == 1:
            lcd4 = lcd_i2c.lcd(pi, width=int(hbl.DISPLAY_display6_width), addr=int(hbl.DISPLAY_display6_address,0))
            delays.ms(100) 
            lcd4.put_line(0, "HBL")  
            lcd4.put_line(3, hbl.DISPLAY_display6_address) 

    except Exception as inst: 

        log.escribeSeparador(hbl.LOGS_hbli2c) 
        log.escribeLineaLog(hbl.LOGS_hbli2c, "Error display addr : " + hbl.DISPLAY_display6_address)
        log.escribeLineaLog(hbl.LOGS_hbli2c, "Error : " + str(inst))

    try:
        if hbl.DISPLAY_display7_activado == 1:
            lcd4 = lcd_i2c.lcd(pi, width=int(hbl.DISPLAY_display7_width), addr=int(hbl.DISPLAY_display7_address,0))
            delays.ms(100) 
            lcd4.put_line(0, "HBL")  
            lcd4.put_line(3, hbl.DISPLAY_display7_address) 

    except Exception as inst: 

        log.escribeSeparador(hbl.LOGS_hbli2c) 
        log.escribeLineaLog(hbl.LOGS_hbli2c, "Error display addr : " + hbl.DISPLAY_display7_address)
        log.escribeLineaLog(hbl.LOGS_hbli2c, "Error : " + str(inst))

    try:
        if hbl.DISPLAY_display8_activado == 1:
            lcd4 = lcd_i2c.lcd(pi, width=int(hbl.DISPLAY_display8_width), addr=int(hbl.DISPLAY_display8_address,0))
            delays.ms(100) 
            lcd4.put_line(0, "HBL")  
            lcd4.put_line(3, hbl.DISPLAY_display8_address) 

    except Exception as inst: 

        log.escribeSeparador(hbl.LOGS_hbli2c) 
        log.escribeLineaLog(hbl.LOGS_hbli2c, "Error display addr : " + hbl.DISPLAY_display8_address)
        log.escribeLineaLog(hbl.LOGS_hbli2c, "Error : " + str(inst))
    
    
