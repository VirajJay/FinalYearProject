#!/bin/sh
sudo pkill wpa_supplicant
sudo wpa_supplicant -Dwext -c /home/pi/Desktop/eduroam.conf -i wlan0 &
