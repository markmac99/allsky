to install the software as a service
edit the files to ensure the paths are all correct
copy allsky.service to /lib/systemd/system
copy allsky.conf to /etc/rsyslogd.d
copy allsky to /etc/logrotate.d

make all the files owned by root and with 644 permissions

then as root, run
systemctl daemon-reload
service rsyslog restart
service allsky restart
