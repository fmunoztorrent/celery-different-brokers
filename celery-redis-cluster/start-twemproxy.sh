#!/bin/sh

# Establecer el límite de descriptores de archivos
ulimit -n 65536

# Ejecutar Twemproxy
exec /usr/local/sbin/nutcracker -c /etc/nutcracker/nutcracker.yml -s 22122
