# Usa una imagen base de ActiveMQ
FROM rmohr/activemq:latest

# Copia el archivo de configuración XML a la imagen
COPY activemq.xml /opt/activemq/conf/activemq.xml

# Expone los puertos necesarios
EXPOSE 61616 8161 61613

# Comando para iniciar ActiveMQ
CMD ["/opt/activemq/bin/activemq", "console"]