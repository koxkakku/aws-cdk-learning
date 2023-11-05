#!/bin/bash

sudo su
yum update -y
yum install httpd -y
systemctl start httpd
systemctl enable httpd

echo "Hello from cdk web server" > /var/www/html/index.html