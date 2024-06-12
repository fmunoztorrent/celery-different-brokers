import stomp
import time

class MyListener(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print('received an error: %s' % message)
    def on_message(self, headers, message):
        print('received a message: %s' % message)

conn = stomp.Connection([('localhost', 61613)])
conn.set_listener('', MyListener())
conn.connect('admin', 'admin', wait=True)

# Enviar un mensaje a la cola 'default'
conn.send(body='Hola, ActiveMQ!', destination='/queue/default')

# Asegurarse de que el mensaje ha sido enviado
time.sleep(2)
conn.disconnect()
