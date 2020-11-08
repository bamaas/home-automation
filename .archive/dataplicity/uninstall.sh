# disable
sudo rm -f /etc/supervisor/conf.d/tuxtunnel.conf
sudo service supervisor restart
# uninstall
sudo apt-get purge supervisor
sudo rm -r /opt/dataplicity
sudo rm -r /etc/supervisor
#sudo reboot