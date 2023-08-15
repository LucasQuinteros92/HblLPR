#!/bin/sh

sudo su <<EOF

# deshabilitar la configuracion de conexion compartida de 4G a Ethernet

# Configuración reenvío

# disable packet forwarding for IPv4
awk '{sub("net.ipv4.ip_forward=1","#net.ipv4.ip_forward=1")}1' /etc/sysctl.conf > temp.txt && mv temp.txt /etc/sysctl.conf --force

# Configurar dnsmasq
# Realizar un backup de la configuración
mv /etc/dnsmasq.conf.orig /etc/dnsmasq.conf  

# Editar las tablas ip4 
# descomenta la linea original para que se active la funcion
awk '{sub("iptables-restore < /etc/iptables.ipv4.nat","#iptables-restore < /etc/iptables.ipv4.nat")}1' /etc/rc.local > /home/pi/temp.txt && mv /home/pi/temp.txt /etc/rc.local --force

# le doy permisos al archivo para su ejecucion
chmod 755 /etc/rc.local

reboot

EOF