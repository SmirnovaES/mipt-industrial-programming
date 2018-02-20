import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit', port=5672))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='aaa')
print(" [x] Sent 'Hello World!'")

connection.close()
