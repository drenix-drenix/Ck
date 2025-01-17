#!/bin/bash
# Only for CentOS
# root?
if [[ $EUID -ne 0 ]]; then
  echo -e "MUST RUN AS ROOT USER! use sudo"
  exit 1
fi
set -e  # stop script if something goes wrong
# open ports
echo "Do you want to open all ports? (y/n)"
read -r open_port
case $open_port in
[yY] | [yY][Ee][Ss] )
	yum update -y
	yum install firewalld -y
	firewall-cmd --zone=public --permanent --add-port=1-65535/udp
	firewall-cmd --zone=public --permanent --add-port=1-65535/tcp
	firewall-cmd --reload
	firewall-cmd --zone=public --list-all
	systemctl enable firewalld
	systemctl restart firewalld
	echo "Check the list above, ports must be open"
	;;
[nN] | [n|N][O|o] )
	echo "Okey, ports are closed"
	;;
*)
	echo "Port won't be open (enter to continue)"
	read -sn1
	;;
esac
# openssl
yum install openssl wget -y
mkdir -p /etc/ssl/v2ray/
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/v2ray/priv.key -out /etc/ssl/v2ray/cert.pub -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=www.example.com"
# x2-ui
yum install curl -y
bash <(curl -Ls https://raw.githubusercontent.com/vaxilu/x-ui/master/install.sh)
x-ui start
# info
yourip=`wget -qO - icanhazip.com`
echo "go to http://$yourip:54321 and set it up" | tee -a /root/v2rayOpenSSL.info
echo "admin admin is login and password" | tee -a /root/v2rayOpenSSL.info
echo "certificate file path: /etc/ssl/v2ray/cert.pub" | tee -a /root/v2rayOpenSSL.info
echo "key file path: /etc/ssl/v2ray/priv.key" | tee -a /root/v2rayOpenSSL.info
echo "" | tee -a /root/v2rayOpenSSL.info
echo "to see that again: cat /root/v2rayOpenSSL.info"
