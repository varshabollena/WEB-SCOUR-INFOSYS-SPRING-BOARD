import pika #it is a python client library used to communicate with RabbitMQ

#creating a connection with RabbitMQ
connection=pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
#channels are used to send and receive the messages
channel=connection.channel()

#declaring queue name and durable
channel.queue_declare(queue='url_queue',durable=True)

#list of urls which are act as starting point
seed_urls=[
    "https://www.w3schools.com/",
    "https://www.geeksforgeeks.org/",
    "https://docs.python.org/"
]

#publish url into RabbitMQ queue
for url in seed_urls:
    channel.basic_publish(
        exchange='',   #default exchange
        routing_key='url_queue',  #routes message to queue
        body=url   #body contains the url
    )
    print(f"[PRODUCER] Sent URL:{url}")
connection.close()