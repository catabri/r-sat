sudo apt-get install gpsd gpsd-clients
sudo systemctl stop gpsd.socket
sudo systemctl disable gps.socket
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
sgps -s
