#!/bin/sh

sudo su <<EOF

# configuracion de conexion compartida de eth1 a eth0 - conexion a la web con eth1

# Configuración reenvío

# enable packet forwarding for IPv4
awk '{sub("#net.ipv4.ip_forward=1","net.ipv4.ip_forward=1")}1' /etc/sysctl.conf > temp.txt && mv temp.txt /etc/sysctl.conf --force

# Configurar dnsmasq
# Realizar un backup de la configuración
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.ETH1

# Editar el archivo de configuración
echo "# Use interface eth0" >> /etc/dnsmasq.conf
echo "interface=eth0" >> /etc/dnsmasq.conf
echo "# listen on" >> /etc/dnsmasq.conf
echo "listen-address=192.168.1.1" >> /etc/dnsmasq.conf
echo "# Bind to the interface to make sure we aren't sending things elsewhere" >> /etc/dnsmasq.conf
echo "#### bind-interfaces #### BUT don't enable this." >> /etc/dnsmasq.conf
echo "# Forward DNS requests to Google DNS" >> /etc/dnsmasq.conf
echo "server=8.8.8.8" >> /etc/dnsmasq.conf
echo "# Don't forward short names" >> /etc/dnsmasq.conf
echo "domain-needed" >> /etc/dnsmasq.conf
echo "# Never forward addresses in the non-routed address spaces." >> /etc/dnsmasq.conf
echo "bogus-priv" >> /etc/dnsmasq.conf
echo "# Assign IP addresses between 192.168.1.2 and 192.168.1.100" >> /etc/dnsmasq.conf
echo "dhcp-range=192.168.1.2,192.168.1.100" >> /etc/dnsmasq.conf

# Configurar NAT
iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE  && sudo iptables -A FORWARD -i eth1 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT && sudo iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT

# Hacer las reglas persistentes
sh -c "iptables-save > /etc/iptables.ipv4.nat"

# Editar las tablas ip4 
# descomenta la linea original para que se active la funcion
awk '{sub("#iptables-restore < /etc/iptables.ipv4.nat","iptables-restore < /etc/iptables.ipv4.nat")}1' /etc/rc.local > /home/pi/temp.txt && mv /home/pi/temp.txt /etc/rc.local --force

# le doy permisos al archivo para su ejecucion
chmod 755 /etc/rc.local

reboot

EOF

 