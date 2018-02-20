import pika
import psycopg2

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit', port=5672))
channel = connection.channel()
print("I'm here")
channel.queue_declare(queue='hello')

db_conn = psycopg2.connect("dbname=my_db user=db_usr password=mysecretpassword host=db port=5432")

def callback(ch, method, properties, body):
    cur = db_conn.cursor()
    cur.execute("INSERT INTO my_table(body) VALUES (%r)" % body)
    db_conn.commit()   
    print(" [x] Received %r" % body)

cur = db_conn.cursor()
cur.execute("CREATE TABLE my_table (body NOT NULL)")
db_conn.commit()

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print('waiting')
channel.start_consuming()
