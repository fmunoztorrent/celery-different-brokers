import stomp
import time

class MyListener(stomp.ConnectionListener):
    def on_error(self, frame):
        print('received an error: %s' % frame.body)
    def on_message(self, frame):
        print('received a message: %s' % frame.body)

conn = stomp.Connection([('localhost', 61613)])
conn.set_listener('', MyListener())
conn.connect('admin', 'admin', wait=True)

# Suscribirse a la cola 'default'
conn.subscribe(destination='/queue/default', id=1, ack='auto')

# Esperar para recibir mensajes
time.sleep(1000)
conn.disconnect()
