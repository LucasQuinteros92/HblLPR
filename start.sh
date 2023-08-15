#!/bin/sh

cd /
cd /usr/programas/hbl
sudo pigpiod &
sudo python3 main.py &