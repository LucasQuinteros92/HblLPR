# HBL - Apertura de barrera por doble factor Patente-DNI

## Lectura de patente
En el modulo serial.py se lee el puerto serie y extrea la patente del mensaje que envia el LPR.
Cada lectura de patente se guardara en una lista listaPatentes[] que sera global a todo el programa

### Configuración de la camara
En la camara se debe poner com-push

## Lectura DNI

La lectura de DNI se hace por Wiegand. Cada lectura se guardara en una lista listaDNIs[] que sera global en todo el programa.

## Validación de Doble Factor
