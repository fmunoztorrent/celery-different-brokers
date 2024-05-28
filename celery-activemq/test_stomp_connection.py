import stomp
import os

def connect_and_send():
    activemq_host = os.getenv('ACTIVEMQ_HOST', 'localhost')
    activemq_port = int(os.getenv('ACTIVEMQ_PORT', 61613))
    activemq_username = os.getenv('ACTIVEMQ_USERNAME', 'admin')
    activemq_password = os.getenv('ACTIVEMQ_PASSWORD', 'admin')

    conn = stomp.Connection([(activemq_host, activemq_port)])
    conn.connect(username=activemq_username, passcode=activemq_password, wait=True)

    conn.send(body='Test message', destination='/queue/test')
    print("Message sent to /queue/test")

    conn.disconnect()

if __name__ == "__main__":
    connect_and_send()
