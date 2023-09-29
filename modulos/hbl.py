import json
import os
import log
import sys

""" --------------------------------------------------------------------------------------------


   Cargar parametros del JSON en memoria


-------------------------------------------------------------------------------------------- """
   
def cargarParametros(archivo):
 
    global REPORTE_idNitro4       
    global REPORTE_lastUpdate 
    global REPORTE_tiempoUpdate 
    global REPORTE_activado 
    global REPORTE_timeOutRequest 
    global REPORTE_encodeAutorization
    global REPORTE_URLToken 
    global REPORTE_URLChequeoConfiguracion 
    global REPORTE_URLReporteInicial 
    global REPORTE_URLReporte   
    global REPORTE_versionFirmware 
    global REPORTE_comandoBash  
    global REPORTE_readLogs  
    global REPORTE_borrarTemp

    global WD_port0_activado
    global WD_port0_esperaSenial
    global WD_port0_bits
    global WD_port0_pin_WD0
    global WD_port0_pin_WD1
    global WD_port0_delayPulso
    global WD_port0_delayIntervalo
    global WD_port0_primerBit 
    global WD_port0_mascara_activada 
    global WD_port0_mascara_valor

    global WD_port1_activado
    global WD_port1_esperaSenial
    global WD_port1_bits
    global WD_port1_pin_WD0
    global WD_port1_pin_WD1
    global WD_port1_delayPulso
    global WD_port1_delayIntervalo
    global WD_port1_primerBit 
    global WD_port1_mascara_activada 
    global WD_port1_mascara_valor
     
    global WD_errorCode
    global WD_URL 
    global WD_ID

    global DIG_in_pushDelay

    global DIG_in_in1_activado
    global DIG_in_in1_pin
    global DIG_in_in1_id

    global DIG_in_in2_activado
    global DIG_in_in2_pin
    global DIG_in_in2_id
  
    global DIG_out_activado 
    global DIG_out_tiempo
    global DIG_out_logica
    global DIG_out_pin_out1
    global DIG_out_pin_out2
    global DIG_out_pin_out3
    global DIG_out_pin_out4
    global DIG_out_pin_out5
    global DIG_out_pin_out6
    global DIG_out_pin_out7
    global DIG_out_pin_out8

    global DIG_led1
    global DIG_led2
    global DIG_led3
    global DIG_buzzer

    global ON
    global OFF

    global SERIAL_COM1_activado
    global SERIAL_COM1_port
    global SERIAL_COM1_baudrate
    global SERIAL_COM1_bytesize
    global SERIAL_COM1_parity
    global SERIAL_COM1_stopbits 
    global SERIAL_COM1_timeout
    
    global SERIAL_COM2_activado
    global SERIAL_COM2_port
    global SERIAL_COM2_baudrate
    global SERIAL_COM2_bytesize
    global SERIAL_COM2_parity
    global SERIAL_COM2_stopbits
    global SERIAL_COM2_timeout
    
    global HID_device1_activado
    global HID_device1_bufferSize 
    global HID_device1_timeout
    global HID_device1_endpoint 
    global HID_device1_vendor_ID
    global HID_device1_product_ID

    global HID_device2_activado 
    global HID_device2_bufferSize 
    global HID_device2_timeout
    global HID_device2_endpoint 
    global HID_device2_vendor_ID
    global HID_device2_product_ID

    global HID_device3_activado 
    global HID_device3_bufferSize 
    global HID_device3_timeout
    global HID_device3_endpoint
    global HID_device3_vendor_ID
    global HID_device3_product_ID

    global HID_device4_activado 
    global HID_device4_bufferSize 
    global HID_device4_timeout
    global HID_device4_endpoint
    global HID_device4_vendor_ID
    global HID_device4_product_ID

    global DISPLAY_display1_activado 
    global DISPLAY_display1_width
    global DISPLAY_display1_address

    global DISPLAY_display2_activado 
    global DISPLAY_display2_width
    global DISPLAY_display2_address

    global DISPLAY_display3_activado 
    global DISPLAY_display3_width
    global DISPLAY_display3_address

    global DISPLAY_display4_activado 
    global DISPLAY_display4_width
    global DISPLAY_display4_address   

    global DISPLAY_display5_activado 
    global DISPLAY_display5_width
    global DISPLAY_display5_address

    global DISPLAY_display6_activado 
    global DISPLAY_display6_width
    global DISPLAY_display6_address

    global DISPLAY_display7_activado 
    global DISPLAY_display7_width
    global DISPLAY_display7_address

    global DISPLAY_display8_activado 
    global DISPLAY_display8_width
    global DISPLAY_display8_address 

    global TCP_serverDefault_ip 
    global TCP_serverDefault_port 
    global TCP_serverDefault_activado 
    global TCP_serverDefault_bufferRX 
    global TCP_serverDefault_intentosConexion 

    global HTTP_server_activado
    global HTTP_server_port
    global HTTP_server_reles 
    global HTTP_server_respuesta
  
    global MOCK_activado
    global MOCK_url
    global FUNC_modo
    
    global REQ_activado
    global REQ_seleccionURL
    global REQ_urlRequest1
    global REQ_urlRequest2
    global REQ_urlRequest3
    global REQ_urlRequest4
    global REQ_urlRequest5
    global REQ_modoRequest
    global REQ_urlError
    global REQ_timeoutRequest
    global REQ_timerActivado 

    global LOGS_pathBackup 
    global LOGS_tamanioRotator 
    global LOGS_hblCore  
    global LOGS_hblConexiones
    global LOGS_hblWiegand
    global LOGS_hblTcp
    global LOGS_hblEntradas
    global LOGS_hblHTTP
    global LOGS_hblReporte
    global LOGS_hblhidDevice
    global LOGS_hbli2c
    global LOGS_FTP
    global LOGS_hblRedundancia
    global LOGS_hblSerial
    global LOGS_hblCacheo
    global LOGS_hblRequest
    global LOGS_hblDobleFactor
    global LOGS_WebSocket
    global LOGS_FileManage
    global LOGS_Salidas
    
 
    global HBLCORE_hblDisplay_activado
    global HBLCORE_hblDisplay_modo 
    global HBLCORE_serialNumber 
    global HBLCORE_revision 
    global HBLCORE_MAC_ethernet 
    global HBLCORE_NTP 
    global HBLCORE_reset_tiempoReset
    global HBLCORE_reset_resetActivado
    global HBLCORE_tamper_activado

    global DEBUG    
    global versionHBL
    global HblID

    global NETWORK_activado

    global NETWORK_eth0_activado
    global NETWORK_eth0_dhcp
    global NETWORK_eth0_static_ip_address
    global NETWORK_eth0_static_routers
    global NETWORK_eth0_netmask
    global NETWORK_eth0_network
    global NETWORK_eth0_broadcast 
    global NETWORK_eth0_metric
    global NETWORK_eth0_DNS
    global NETWORK_eth0_gateway
    
    global NETWORK_eth1_activado
    global NETWORK_eth1_dhcp
    global NETWORK_eth1_static_ip_address
    global NETWORK_eth1_static_routers
    global NETWORK_eth1_netmask
    global NETWORK_eth1_network
    global NETWORK_eth1_broadcast 
    global NETWORK_eth1_metric
    global NETWORK_eth1_vendor_ID 
    global NETWORK_eth1_product_ID 
    global NETWORK_eth1_timeDelay

    global NETWORK_wlan0_activado
    global NETWORK_wlan0_dhcp
    global NETWORK_wlan0_static_ip_address
    global NETWORK_wlan0_static_routers
    global NETWORK_wlan0_metric 
    global NETWORK_wlan0_ssid
    global NETWORK_wlan0_password  
 
    global NETWORK_ppp0_activado
    global NETWORK_ppp0_vendor_ID 
    global NETWORK_ppp0_product_ID  
    global NETWORK_ppp0_dialcommand
    global NETWORK_ppp0_init1
    global NETWORK_ppp0_init2
    global NETWORK_ppp0_init3
    global NETWORK_ppp0_init4
    global NETWORK_ppp0_stupidmode
    global NETWORK_ppp0_ISDN
    global NETWORK_ppp0_modemType
    global NETWORK_ppp0_askPassword
    global NETWORK_ppp0_phone 
    global NETWORK_ppp0_username
    global NETWORK_ppp0_password
    global NETWORK_ppp0_baud
    global NETWORK_ppp0_newPPPD 
    global NETWORK_ppp0_carrierCheck
    global NETWORK_ppp0_autoReconnect  
    global NETWORK_ppp0_dialAttempts 
    global NETWORK_ppp0_metric

    global NETWORK_testConexion_activado 
    global NETWORK_testConexion_url 
    global NETWORK_testConexion_timeoutUrl
    global NETWORK_testConexion_timeDelay
    global NETWORK_testConexion_timeRepeat 
    global NETWORK_testConexion_intentosConexion  
    global NETWORK_testConexion_resetActivado

    global FTP_activado
    global FTP_server
    global FTP_user
    global FTP_pass 

    global REDUNDANCIA_primeraLetraUnidad
    global REDUNDANCIA_ultimaLetraUnidad
    global REDUNDANCIA_primeraParticion
    global REDUNDANCIA_ultimaParticion

    global CACHEO_activado
    global CACHEO_cantidadCacheos
    global CACHEO_cacheosPositivos
    global CACHEO_tiempoRelePositivo
    global CACHEO_repRelePositivo
    global CACHEO_tiempoReleNegativo
    global CACHEO_repReleNegativo
    
    global Validacion_Doble_Factor_activado 
    global Validacion_Doble_Factor_periodReport
    global Validacion_Doble_Factor_reportFile
    global Validacion_Doble_Factor_JSONBBDDPATH
    
    global WebSocket_activado
    global WebSocket_WebSocket_Host
    global WebSocket_Api_Host
    global WebSocket_Tipo_Evento
    global WebSocket_Device_ID
    global WebSocket_User
    global WebSocket_Password
    global WebSocket_Header           
   
    global WebSocket_Token
    global WebSocket_ClientName       
    global WebSocket_ClientId               
    # ******************************************************************************************************************************************
    

    # variable para guardar que pantalla esta activa
    global pantallaOled

    pantallaOled = 1
  

    # ******************************************************************************************************************************************
    #   Inicio de la carga de datos en las variables
    # ******************************************************************************************************************************************

    # path del archivo
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) 
 

    # Leo los parametros de configuracion en el JSON
    with open(os.path.join(__location__ , archivo), "r") as f:
        data = json.load(f)
  
    # reporte
    REPORTE_idNitro4=data["reporte"]["idNitro4"]       
    REPORTE_lastUpdate=data["reporte"]["lastUpdate"]  
    REPORTE_tiempoUpdate=data["reporte"]["tiempoUpdate"]
    REPORTE_activado=data["reporte"]["activado"]   
    REPORTE_timeOutRequest=data["reporte"]["timeOutRequest"]  
    REPORTE_encodeAutorization=data["reporte"]["encodeAutorization"]
    REPORTE_URLToken=data["reporte"]["URLToken"]
    REPORTE_URLChequeoConfiguracion=data["reporte"]["URLChequeoConfiguracion"] 
    REPORTE_URLReporteInicial=data["reporte"]["URLReporteInicial"]
    REPORTE_URLReporte=data["reporte"]["URLReporte"]

    REPORTE_versionFirmware=data["reporte"]["versionFirmware"] 
    REPORTE_comandoBash=data["reporte"]["comandoBash"]
    REPORTE_readLogs=data["reporte"]["readLogs"]   
    REPORTE_borrarTemp=data["reporte"]["borrarTemp"]

    #  Seleccion de funcionamiento hbl
    #
    #   0  :  repetidor wiegand IN : port0 -> OUT : port1
    #   1  :  funcionamiento supeditado al request - IN : port0 -> OUT : port1
    #   2  :  decodificador wiegand port0 - TCP
    #   3  :  decodificador wiegand port0 - decodificador wiegand port1
    #   4  :  hidDevice Teclado - Display LCD - TCP
    #   5  :  lector DNI HID -> wiegand 34
    #   6  :  decodificador wiegand port0 -> envio ID con request a URL (test lector Tags RFID)
    #   7  :  conexion TCP con minipc para envio de datos del teclado
    #   8  :  lectura serial de lector de dni 2D -> envio wiegand 34 al reloj

    FUNC_modo=data["funcionamiento"]["modo"]  
    
    # wiegand
    WD_port0_activado=data["wiegand"]["port0"]["activado"]
    WD_port0_esperaSenial=data["wiegand"]["port0"]["esperaSenial"]
    WD_port0_bits=data["wiegand"]["port0"]["bits"]
    WD_port0_pin_WD0=data["wiegand"]["port0"]["pin"]["WD0"]
    WD_port0_pin_WD1=data["wiegand"]["port0"]["pin"]["WD1"]
    WD_port0_delayPulso=data["wiegand"]["port0"]["delayPulso"]
    WD_port0_delayIntervalo=data["wiegand"]["port0"]["delayIntervalo"]
    WD_port0_primerBit=data["wiegand"]["port0"]["primerBit"]
    WD_port0_mascara_activada=data["wiegand"]["port0"]["mascara"]["activada"]
    WD_port0_mascara_valor=data["wiegand"]["port0"]["mascara"]["valor"]

    WD_port1_activado=data["wiegand"]["port1"]["activado"]
    WD_port1_esperaSenial=data["wiegand"]["port1"]["esperaSenial"]
    WD_port1_bits=data["wiegand"]["port1"]["bits"]
    WD_port1_pin_WD0=data["wiegand"]["port1"]["pin"]["WD0"]
    WD_port1_pin_WD1=data["wiegand"]["port1"]["pin"]["WD1"]
    WD_port1_delayPulso=data["wiegand"]["port1"]["delayPulso"]
    WD_port1_delayIntervalo=data["wiegand"]["port1"]["delayIntervalo"]
    WD_port1_primerBit=data["wiegand"]["port1"]["primerBit"]
    WD_port1_mascara_activada=data["wiegand"]["port1"]["mascara"]["activada"]
    WD_port1_mascara_valor=data["wiegand"]["port1"]["mascara"]["valor"]

    WD_errorCode=data["wiegand"]["errorCode"]
    WD_URL=data["wiegand"]["URL"]
    WD_ID=data["wiegand"]["ID"]
    WD_URL_timeOutRequest=data["wiegand"]["URL_timeOutRequest"]
  
    # digital
    DIG_in_pushDelay=data["digital"]["in"]["pushDelay"] 
    DIG_in_in1_activado=data["digital"]["in"]["in1"]["activado"]
    DIG_in_in1_pin=data["digital"]["in"]["in1"]["pin"]
    DIG_in_in1_id=data["digital"]["in"]["in1"]["id"]

    DIG_in_in2_activado=data["digital"]["in"]["in2"]["activado"]
    DIG_in_in2_pin=data["digital"]["in"]["in2"]["pin"]
    DIG_in_in2_id=data["digital"]["in"]["in2"]["id"]
 
    DIG_out_activado=data["digital"]["out"]["activado"]
    DIG_out_tiempo=data["digital"]["out"]["tiempo"]
    DIG_out_logica=data["digital"]["out"]["logica"]
    DIG_out_pin_out1=data["digital"]["out"]["pin"]["out1"]
    DIG_out_pin_out2=data["digital"]["out"]["pin"]["out2"]
    DIG_out_pin_out3=data["digital"]["out"]["pin"]["out3"]
    DIG_out_pin_out4=data["digital"]["out"]["pin"]["out4"]
    DIG_out_pin_out5=data["digital"]["out"]["pin"]["out5"]
    DIG_out_pin_out6=data["digital"]["out"]["pin"]["out6"]
    DIG_out_pin_out7=data["digital"]["out"]["pin"]["out7"]
    DIG_out_pin_out8=data["digital"]["out"]["pin"]["out8"]
    
    DIG_led1=data["digital"]["userLeds"]["led1"]["pin"]
    DIG_led2=data["digital"]["userLeds"]["led2"]["pin"]
    DIG_led3=data["digital"]["userLeds"]["led3"]["pin"]
    DIG_buzzer=data["digital"]["userLeds"]["buzzer"]["pin"]
    
    # define la logica si es inversa o directa
    if DIG_out_logica == 0:
        ON = 1
        OFF = 0
    else :   
        ON = 0
        OFF = 1
    
    # serial
    SERIAL_COM1_activado    =data["serial"]["COM1"]["activado"]
    SERIAL_COM1_port        =data["serial"]["COM1"]["port"]
    SERIAL_COM1_baudrate    =data["serial"]["COM1"]["baudrate"]
    SERIAL_COM1_bytesize    =data["serial"]["COM1"]["bytesize"]
    SERIAL_COM1_parity      =data["serial"]["COM1"]["parity"]
    SERIAL_COM1_stopbits    =data["serial"]["COM1"]["stopbits"] 
    SERIAL_COM1_timeout     =data["serial"]["COM1"]["timeout"]

    SERIAL_COM2_activado    =data["serial"]["COM2"]["activado"]
    SERIAL_COM2_port        =data["serial"]["COM2"]["port"]
    SERIAL_COM2_baudrate    =data["serial"]["COM2"]["baudrate"]
    SERIAL_COM2_bytesize    =data["serial"]["COM2"]["bytesize"]
    SERIAL_COM2_parity      =data["serial"]["COM2"]["parity"]
    SERIAL_COM2_stopbits    =data["serial"]["COM2"]["stopbits"]  
    SERIAL_COM2_timeout     =data["serial"]["COM2"]["timeout"]
    
    # hidDevices   
    HID_device1_activado=data["hidDevices"]["device1"]["activado"]
    HID_device1_bufferSize=data["hidDevices"]["device1"]["bufferSize"]
    HID_device1_timeout=data["hidDevices"]["device1"]["timeout"]
    HID_device1_endpoint=data["hidDevices"]["device1"]["endpoint"]
    HID_device1_vendor_ID=data["hidDevices"]["device1"]["vendor_ID"]
    HID_device1_product_ID=data["hidDevices"]["device1"]["product_ID"]

    HID_device2_activado=data["hidDevices"]["device2"]["activado"]
    HID_device2_bufferSize=data["hidDevices"]["device2"]["bufferSize"]
    HID_device2_timeout=data["hidDevices"]["device2"]["timeout"]
    HID_device2_endpoint=data["hidDevices"]["device2"]["endpoint"]
    HID_device2_vendor_ID=data["hidDevices"]["device2"]["vendor_ID"]
    HID_device2_product_ID=data["hidDevices"]["device2"]["product_ID"]

    HID_device3_activado=data["hidDevices"]["device3"]["activado"]
    HID_device3_bufferSize=data["hidDevices"]["device3"]["bufferSize"]
    HID_device3_timeout=data["hidDevices"]["device3"]["timeout"]
    HID_device3_endpoint=data["hidDevices"]["device3"]["endpoint"]
    HID_device3_vendor_ID=data["hidDevices"]["device3"]["vendor_ID"]
    HID_device3_product_ID=data["hidDevices"]["device3"]["product_ID"]

    HID_device4_activado=data["hidDevices"]["device4"]["activado"]
    HID_device4_bufferSize=data["hidDevices"]["device4"]["bufferSize"]
    HID_device4_timeout=data["hidDevices"]["device4"]["timeout"]
    HID_device4_endpoint=data["hidDevices"]["device4"]["endpoint"]
    HID_device4_vendor_ID=data["hidDevices"]["device4"]["vendor_ID"]
    HID_device4_product_ID=data["hidDevices"]["device4"]["product_ID"]

    # displays
    DISPLAY_display1_activado=data["display"]["display1"]["activado"]
    DISPLAY_display1_width=data["display"]["display1"]["width"]
    DISPLAY_display1_address=data["display"]["display1"]["address"]

    DISPLAY_display2_activado=data["display"]["display2"]["activado"]
    DISPLAY_display2_width=data["display"]["display2"]["width"]
    DISPLAY_display2_address=data["display"]["display2"]["address"]

    DISPLAY_display3_activado=data["display"]["display3"]["activado"]
    DISPLAY_display3_width=data["display"]["display3"]["width"]
    DISPLAY_display3_address=data["display"]["display3"]["address"]

    DISPLAY_display4_activado=data["display"]["display4"]["activado"]
    DISPLAY_display4_width=data["display"]["display4"]["width"]
    DISPLAY_display4_address=data["display"]["display4"]["address"]

    DISPLAY_display5_activado=data["display"]["display5"]["activado"]
    DISPLAY_display5_width=data["display"]["display5"]["width"]
    DISPLAY_display5_address=data["display"]["display5"]["address"]

    DISPLAY_display6_activado=data["display"]["display6"]["activado"]
    DISPLAY_display6_width=data["display"]["display6"]["width"]
    DISPLAY_display6_address=data["display"]["display6"]["address"]

    DISPLAY_display7_activado=data["display"]["display7"]["activado"]
    DISPLAY_display7_width=data["display"]["display7"]["width"]
    DISPLAY_display7_address=data["display"]["display7"]["address"]

    DISPLAY_display8_activado=data["display"]["display8"]["activado"]
    DISPLAY_display8_width=data["display"]["display8"]["width"]
    DISPLAY_display8_address=data["display"]["display8"]["address"]

    # tcp 
    TCP_serverDefault_ip=data["tcp"]["serverDefault"]["ip"]
    TCP_serverDefault_port=data["tcp"]["serverDefault"]["port"]
    TCP_serverDefault_activado=data["tcp"]["serverDefault"]["activado"]
    TCP_serverDefault_bufferRX=data["tcp"]["serverDefault"]["bufferRX"]
    TCP_serverDefault_intentosConexion=data["tcp"]["serverDefault"]["intentosConexion"] 

    # http
    HTTP_server_activado=data["http"]["server"]["activado"]
    HTTP_server_port=data["http"]["server"]["port"]
    HTTP_server_reles=data["http"]["server"]["reles"] 
    HTTP_server_respuesta=data["http"]["server"]["respuesta"] 

    # mock
    MOCK_activado=data["mock"]["activado"] 
    MOCK_url=data["mock"]["url"] 
  
    # request
    REQ_activado=data["request"]["activado"] 
    REQ_seleccionURL=data["request"]["seleccionURL"] 
    REQ_urlRequest1=data["request"]["urlRequest1"] 
    REQ_urlRequest2=data["request"]["urlRequest2"] 
    REQ_urlRequest3=data["request"]["urlRequest3"] 
    REQ_urlRequest4=data["request"]["urlRequest4"] 
    REQ_urlRequest5=data["request"]["urlRequest5"] 
    REQ_modoRequest=data["request"]["modoRequest"]

    REQ_urlError=data["request"]["urlError"] 
    REQ_timeoutRequest=data["request"]["timeoutRequest"] 
    REQ_timerActivado=data["request"]["timerActivado"]

    # log   
    LOGS_pathBackup=data["logs"]["pathBackup"] 
    LOGS_tamanioRotator=data["logs"]["tamanioRotator"] 
    LOGS_hblCore=data["logs"]["hblCore"]  
    LOGS_hblConexiones=data["logs"]["hblConexiones"] 
    LOGS_hblWiegand=data["logs"]["hblWiegand"] 
    LOGS_hblTcp=data["logs"]["hblTcp"] 
    LOGS_hblEntradas=data["logs"]["hblEntradas"] 
    LOGS_hblHTTP=data["logs"]["hblHTTP"]  
    LOGS_hblReporte=data["logs"]["hblReporte"]  
    LOGS_hblhidDevice=data["logs"]["hblhidDevice"]  
    LOGS_hbli2c=data["logs"]["hbli2c"] 
    LOGS_FTP=data["logs"]["hblFTP"] 
    LOGS_hblRedundancia=data["logs"]["hblRedundancia"] 
    LOGS_hblSerial=data["logs"]["hblSerial"]   
    LOGS_hblCacheo=data["logs"]["hblCacheo"]   
    LOGS_hblRequest=data["logs"]["hblRequest"] 
    LOGS_hblDobleFactor=data["logs"]["hblDobleFactor"]
    LOGS_WebSocket=data["logs"]["hblWebSocket"]
    LOGS_FileManage = data["logs"]["hblFileManage"]
    LOGS_Salidas    = data["logs"]["hblSalidas"]  

    # hblCore
    HBLCORE_hblDisplay_activado=data["hblCore"]["hblDisplay"]["activado"]
    HBLCORE_hblDisplay_modo=data["hblCore"]["hblDisplay"]["modo"]
    HBLCORE_serialNumber=data["hblCore"]["serialNumber"] 
    HBLCORE_revision=data["hblCore"]["revision"] 
    HBLCORE_MAC_ethernet=data["hblCore"]["MAC_ethernet"] 
    HBLCORE_NTP=data["hblCore"]["NTP"] 
    HBLCORE_reset_resetActivado=data["hblCore"]["reset"]["resetActivado"] 
    HBLCORE_reset_tiempoReset=data["hblCore"]["reset"]["tiempoReset"] 
    HBLCORE_tamper_activado=data["hblCore"]["tamper"]["activado"] 
 
    DEBUG     =data["debug"]  
    versionHBL=data["versionHBL"]  
    HblID     =data["HBLNAME_ID"]
    
    # network
    NETWORK_activado=data["network"]["activado"]

    NETWORK_eth0_activado=data["network"]["eth0"]["activado"]
    NETWORK_eth0_dhcp=data["network"]["eth0"]["dhcp"]
    NETWORK_eth0_static_ip_address=data["network"]["eth0"]["static_ip_address"]
    NETWORK_eth0_static_routers=data["network"]["eth0"]["static_routers"]
    NETWORK_eth0_netmask=data["network"]["eth0"]["netmask"]
    NETWORK_eth0_network=data["network"]["eth0"]["network"]
    NETWORK_eth0_broadcast=data["network"]["eth0"]["broadcast"]  
    NETWORK_eth0_metric=data["network"]["eth0"]["metric"]
    NETWORK_eth0_gateway= data["network"]["eth0"]["gateway"]
    NETWORK_eth0_DNS = data["network"]["eth0"]["DNS"]

    NETWORK_eth1_activado=data["network"]["eth1"]["activado"]
    NETWORK_eth1_dhcp=data["network"]["eth1"]["dhcp"]
    NETWORK_eth1_static_ip_address=data["network"]["eth1"]["static_ip_address"]
    NETWORK_eth1_static_routers=data["network"]["eth1"]["static_routers"]
    NETWORK_eth1_netmask=data["network"]["eth1"]["netmask"]
    NETWORK_eth1_network=data["network"]["eth1"]["network"]
    NETWORK_eth1_broadcast=data["network"]["eth1"]["broadcast"]  
    NETWORK_eth1_metric=data["network"]["eth1"]["metric"]
    NETWORK_eth1_vendor_ID=data["network"]["eth1"]["vendor_ID"]  
    NETWORK_eth1_product_ID=data["network"]["eth1"]["product_ID"] 
    NETWORK_eth1_timeDelay=data["network"]["eth1"]["timeDelay"] 

    NETWORK_wlan0_activado=data["network"]["wlan0"]["activado"]
    NETWORK_wlan0_dhcp=data["network"]["wlan0"]["dhcp"]
    NETWORK_wlan0_static_ip_address=data["network"]["wlan0"]["static_ip_address"]
    NETWORK_wlan0_static_routers=data["network"]["wlan0"]["static_routers"]
    NETWORK_wlan0_metric=data["network"]["wlan0"]["metric"]
    NETWORK_wlan0_ssid=data["network"]["wlan0"]["ssid"]
    NETWORK_wlan0_password=data["network"]["wlan0"]["password"] 

    NETWORK_ppp0_activado=data["network"]["ppp0"]["activado"]
    NETWORK_ppp0_vendor_ID=data["network"]["ppp0"]["vendor_ID"]
    NETWORK_ppp0_product_ID=data["network"]["ppp0"]["product_ID"]  
    NETWORK_ppp0_dialcommand=data["network"]["ppp0"]["dialcommand"]
    NETWORK_ppp0_init1=data["network"]["ppp0"]["init1"]
    NETWORK_ppp0_init2=data["network"]["ppp0"]["init2"]
    NETWORK_ppp0_init3=data["network"]["ppp0"]["init3"]
    NETWORK_ppp0_init4=data["network"]["ppp0"]["init4"]
    NETWORK_ppp0_stupidmode=data["network"]["ppp0"]["stupidmode"]
    NETWORK_ppp0_ISDN=data["network"]["ppp0"]["ISDN"]
    NETWORK_ppp0_modemType=data["network"]["ppp0"]["modemType"]
    NETWORK_ppp0_askPassword=data["network"]["ppp0"]["askPassword"]
    NETWORK_ppp0_phone=data["network"]["ppp0"]["phone"] 
    NETWORK_ppp0_username=data["network"]["ppp0"]["username"]
    NETWORK_ppp0_password=data["network"]["ppp0"]["password"]
    NETWORK_ppp0_baud=data["network"]["ppp0"]["baud"]
    NETWORK_ppp0_newPPPD=data["network"]["ppp0"]["newPPPD"]
    NETWORK_ppp0_carrierCheck=data["network"]["ppp0"]["carrierCheck"]
    NETWORK_ppp0_autoReconnect=data["network"]["ppp0"]["autoReconnect"] 
    NETWORK_ppp0_dialAttempts=data["network"]["ppp0"]["dialAttempts"] 
    NETWORK_ppp0_metric=data["network"]["ppp0"]["metric"] 
 
    NETWORK_testConexion_activado=data["network"]["testConexion"]["activado"] 
    NETWORK_testConexion_url=data["network"]["testConexion"]["url"] 
    NETWORK_testConexion_timeoutUrl=data["network"]["testConexion"]["timeoutUrl"] 
    NETWORK_testConexion_timeDelay=data["network"]["testConexion"]["timeDelay"] 
    NETWORK_testConexion_timeRepeat=data["network"]["testConexion"]["timeRepeat"] 
    NETWORK_testConexion_intentosConexion=data["network"]["testConexion"]["intentosConexion"] 
    NETWORK_testConexion_resetActivado=data["network"]["testConexion"]["resetActivado"]   

    FTP_activado=data["ftp"]["activado"] 
    FTP_server=data["ftp"]["server"] 
    FTP_user=data["ftp"]["user"] 
    FTP_pass=data["ftp"]["pass"]     

    REDUNDANCIA_primeraLetraUnidad=data["redundancia"]["primeraLetraUnidad"] 
    REDUNDANCIA_ultimaLetraUnidad=data["redundancia"]["ultimaLetraUnidad"] 
    REDUNDANCIA_primeraParticion=data["redundancia"]["primeraParticion"] 
    REDUNDANCIA_ultimaParticion=data["redundancia"]["ultimaParticion"] 

    CACHEO_activado=data["cacheo"]["activado"] 
    CACHEO_cantidadCacheos=data["cacheo"]["cantidadCacheos"]
    CACHEO_cacheosPositivos=data["cacheo"]["cacheosPositivos"]
    CACHEO_tiempoRelePositivo=data["cacheo"]["tiempoRelePositivo"]
    CACHEO_repRelePositivo=data["cacheo"]["repRelePositivo"]
    CACHEO_tiempoReleNegativo=data["cacheo"]["tiempoReleNegativo"]
    CACHEO_repReleNegativo=data["cacheo"]["repReleNegativo"]


    Validacion_Doble_Factor_activado        =data["Validacion_Doble_Factor"]["activado"] 
    Validacion_Doble_Factor_periodReport    =data["Validacion_Doble_Factor"]["periodReport"]
    Validacion_Doble_Factor_reportFile      =data["Validacion_Doble_Factor"]["reportFile"] 
    Validacion_Doble_Factor_JSONBBDDPATH    =data["Validacion_Doble_Factor"]["JSONBBDDPATH"]
    
    WebSocket_activado          =data["WebSocket"]["activado"]
    WebSocket_WebSocket_Host    =data["WebSocket"]["WebSocket_Host"]
    WebSocket_Api_Host          =data["WebSocket"]["Api_Host"]
    WebSocket_Tipo_Evento       =data["WebSocket"]["Tipo_Evento"]
    WebSocket_Device_ID         =data["WebSocket"]["Device_ID"]
    WebSocket_User              =data["WebSocket"]["User"]
    WebSocket_Password          =data["WebSocket"]["Password"]
    WebSocket_Header            =data["WebSocket"]["header"]
    WebSocket_ClientName        =data["WebSocket"]["ClientName"]
    WebSocket_ClientId          =data["WebSocket"]["ClientId"]
    WebSocket_Token             =data["WebSocket"]["Token"]