import os
from kombu.utils.encoding import bytes_to_str
from kombu.transport import virtual
import stomp
import logging

class StompChannel(virtual.Channel):
    def __init__(self, connection, **kwargs):
        super().__init__(connection, **kwargs)
        self._queue_cache = {}
        self.connection = connection
        self._used_channel_ids = []  # Lista en lugar de set para compatibilidad
        self.exchanges = {}
        self.queues = {}
        self.bindings = set()  # Conjunto para almacenar enlaces

    def _new_queue(self, queue, **kwargs):
        self._queue_cache[queue] = []

    def _put(self, queue, message, **kwargs):
        self._queue_cache[queue].append(message)

    def _get(self, queue, timeout=None):
        if queue not in self._queue_cache:
            raise self.Empty()
        try:
            return self._queue_cache[queue].pop(0)
        except IndexError:
            raise self.Empty()

    def exchange_declare(self, exchange, type='direct', durable=False, auto_delete=True, arguments=None, nowait=False, passive=False):
        self.exchanges[exchange] = {
            'type': type,
            'durable': durable,
            'auto_delete': auto_delete,
            'arguments': arguments,
        }

    def queue_declare(self, queue, passive=False, durable=False, exclusive=False, auto_delete=True, arguments=None, nowait=False):
        self.queues[queue] = {
            'durable': durable,
            'exclusive': exclusive,
            'auto_delete': auto_delete,
            'arguments': arguments,
        }
        if queue not in self._queue_cache:
            self._new_queue(queue)

    def queue_bind(self, queue, exchange, routing_key='', arguments=None, nowait=False):
        binding = (queue, exchange, routing_key)
        if binding not in self.bindings:
            self.bindings.add(binding)

    def has_binding(self, queue, exchange, routing_key):
        return (queue, exchange, routing_key) in self.bindings

    def basic_consume(self, queue, no_ack, callback, consumer_tag, on_cancel=None, arguments=None, nowait=False):
        self.connection._callbacks[queue] = callback
        self.connection.subscribe(destination=f'/queue/{queue}', id=consumer_tag, ack='auto' if no_ack else 'client')

class StompConnection(stomp.Connection11):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._used_channel_ids = []  # Lista en lugar de set para compatibilidad
        self.channel_max = 65535
        self.client = self  # Asegurar que client se refiera a sí mismo
        self.transport_options = {}  # Opciones de transporte
        self.state = self  # Añadir atributo state
        self.exchanges = {}  # Añadir atributo exchanges
        self.queues = {}  # Añadir atributo queues
        self.bindings = set()  # Conjunto para almacenar enlaces
        self._callbacks = {}  # Añadir atributo _callbacks
        self._connected = False  # Indicador de conexión
        self.declared_entities = set()  # Añadir atributo declared_entities

    def close_channel(self, channel):
        # Método de cierre de canal requerido por Kombu
        pass

    def has_binding(self, queue, exchange, routing_key):
        return (queue, exchange, routing_key) in self.bindings

    def start(self):
        # Añadir el método start para StompConnection
        pass

    def connect(self, *args, **kwargs):
        if not self._connected:
            super().connect(*args, **kwargs)
            self._connected = True

    def disconnect(self, *args, **kwargs):
        if self._connected:
            super().disconnect(*args, **kwargs)
            self._connected = False

class Transport(virtual.Transport):
    Channel = StompChannel

    def __init__(self, client, **kwargs):
        super().__init__(client, **kwargs)
        self.client = client
        self.connection = None

    def driver_version(self):
        return '1.0'

    def establish_connection(self):
        activemq_host = os.getenv('ACTIVEMQ_HOST', 'localhost')
        activemq_port = int(os.getenv('ACTIVEMQ_PORT', 61613))
        activemq_username = os.getenv('ACTIVEMQ_USERNAME', 'admin')
        activemq_password = os.getenv('ACTIVEMQ_PASSWORD', 'admin')

        logging.info(f"Attempting to connect to ActiveMQ at {activemq_host}:{activemq_port} with username {activemq_username}")

        self.connection = StompConnection([(activemq_host, activemq_port)])
        try:
            self.connection.connect(username=activemq_username, passcode=activemq_password, wait=True)
            logging.info(f"Established connection to host {activemq_host}, port {activemq_port}")
        except stomp.exception.ConnectFailedException as e:
            raise ConnectionError(f"Could not connect to ActiveMQ at {activemq_host}:{activemq_port}") from e
        return self.connection

    def close_connection(self, connection):
        connection.disconnect()

    def create_channel(self, connection):
        return StompChannel(connection)

    def drain_events(self, connection, timeout=None):
        connection.set_listener('', self)
        connection.start()
        connection.connect(wait=True)
        connection.subscribe(destination='/queue/default', id=1, ack='auto')

    def on_message(self, headers, message):
        queue = bytes_to_str(headers['destination'].split('/')[-1])
        self.client._queue_cache[queue].append(message)

    def _get_channel(self):
        """Override this method to return a new channel."""
        return self.create_channel(self.connection)

    def _put_channel(self, channel):
        """Override this method to properly close a channel."""
        channel.close()
