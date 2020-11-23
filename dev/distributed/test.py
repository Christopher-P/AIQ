
#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('chris', 'TdS3g8opiqi9DA7gi')
parameters = pika.ConnectionParameters('10.218.111.4',
                                       5672,
                                       '/',
                                       credentials, socket_timeout=20)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()


"""This method connects to RabbitMQ, returning the connection handle.
When the connection is established, the on_connection_open method
will be invoked by pika.

:rtype: pika.SelectConnection

"""
'''
import pika
import ssl
account = 'opensuse'
server = '69.166.47.174'
credentials = pika.PlainCredentials('chris', 'TdS3g8opiqi9DA7gi')
context = ssl.create_default_context()
ssl_options = pika.SSLOptions(context, server)
parameters = pika.ConnectionParameters(server, 15671, '/', credentials, ssl_options=ssl_options, socket_timeout=10)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
'''