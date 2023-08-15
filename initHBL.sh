#!/bin/sh
sudo su <<EOF
echo "Inicializador HBL"
sleep 5
echo "Actualizando modulos HBL (apt-get update)..." 
apt-get update -y -o Dpkg::Options::="--force-confold"
echo "Actualizando modulos HBL (apt-get upgrade)..."  
apt-get upgrade -y -o Dpkg::Options::="--force-confold" 
echo "Instalando modulo EEPROM update..."
apt-get install rpi-eeprom-update -y  
echo "Modificando archivo configuracion EEPROM..."
cat /dev/null > /etc/default/rpi-eeprom-update
echo 'FIRMWARE_RELEASE_STATUS="stable"' > /etc/default/rpi-eeprom-update
echo "Actualizando EEPROM a ultima version estable..."
rpi-eeprom-update -a
echo "Apagando ..."
sleep 5
shutdown -h 0
EOF