#!/bin/sh
sudo su <<EOF
apt-get update && sudo apt-get upgrade -y
apt-get -y install python3-pip
apt-get install rpi-eeprom-update -y
pip3 install pigpio
apt-get install pigpio -y
pip3 install pyusb
apt-get install dnsmasq -y
apt-get install python-usb python3-usb -y
apt-get install wvdial -y 
pip3 install cbor2 
pip3 install smbus2
pip3 install Pillow
apt-get install libopenjp2-7 -y
apt install libtiff5 -y
apt install git -y
apt-get install dialog -y

timedatectl set-timezone America/Argentina/Buenos_Aires

# desactivacion del switch automatico del modem usb para poder realizarlo manualmente desde el hbl
awk '{sub("DisableSwitching=0","DisableSwitching=1")}1' /etc/usb_modeswitch.conf > temp.txt && mv temp.txt /etc/usb_modeswitch.conf --force

# forzado del hdmi para que inicie la raspberry sin la necesidad de tener conectado un monitor
awk '{sub("#hdmi_force_hotplug=1","hdmi_force_hotplug=1")}1' /boot/config.txt > /home/pi/temp.txt && mv /home/pi/temp.txt /boot/config.txt --force

# habilitacion del bus i2c
awk '{sub("#dtparam=i2c_arm=on","dtparam=i2c_arm=on")}1' /boot/config.txt > /home/pi/temp.txt && mv /home/pi/temp.txt /boot/config.txt --force

# habilitacion del bus spi
awk '{sub("#dtparam=spi=on","dtparam=spi=on")}1' /boot/config.txt > /home/pi/temp.txt && mv /home/pi/temp.txt /boot/config.txt --force

# habilita el modulo uart para la comunicacion Serial
echo "enable_uart=1" >> /boot/config.txt
 
# cambio de password
FIRSTUSER=`getent passwd 1000 | cut -d: -f1`
FIRSTUSERHOME=`getent passwd 1000 | cut -d: -f6`
echo "$FIRSTUSER:"'$5$v/ct2C0c4l$n0ewGbF1fmbMh66XrvHOBkVm5eN0D2CLLgwqxj8Hrt1' | chpasswd -e 

# seteo de propiedades de timezone y el layout del teclado
rm -f /etc/xdg/autostart/piwiz.desktop
rm -f /etc/localtime
echo "America/Buenos_Aires" >/etc/timezone
dpkg-reconfigure -f noninteractive tzdata
cat >/etc/default/keyboard <<'KBEOF'
XKBMODEL="pc105"
XKBLAYOUT="es"
XKBVARIANT=""
XKBOPTIONS=""
KBEOF
dpkg-reconfigure -f noninteractive keyboard-configuration  

# Realizar un backup de la configuración original
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig

# borrar el contenido del archivo /etc/rc.local
cat /dev/null > /etc/rc.local

# editar archivo inicio /etc/rc.local
echo "#!/bin/sh -e" >> /etc/rc.local
echo "#" >> /etc/rc.local
echo "#" >> /etc/rc.local
echo "sh /usr/programas/hbl/start.sh" >> /etc/rc.local
echo "#" >> /etc/rc.local 
echo "#iptables-restore < /etc/iptables.ipv4.nat" >> /etc/rc.local 
echo "#" >> /etc/rc.local
echo "exit 0" >> /etc/rc.local 

# le doy permisos al archivo para su ejecucion
chmod 755 /etc/rc.local

reboot
EOF