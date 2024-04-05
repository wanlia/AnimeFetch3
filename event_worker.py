import os
import pika
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def callback(ch, method, properties, body):
    logging.info(f"Received message: {body.decode()}")

def main():
    cloudamqp_url = os.getenv('CLOUDAMQP_URL')
    if not cloudamqp_url:
        logging.error('CLOUDAMQP_URL is not set.')
        return

    logging.info(f"Attempting to connect to RabbitMQ with URL: {cloudamqp_url}")
    try:
        params = pika.URLParameters(cloudamqp_url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue='anime_updates')
        channel.basic_consume(queue='anime_updates', on_message_callback=callback, auto_ack=True)
        logging.info('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except Exception as e:
        logging.error(f"Failed to connect to RabbitMQ: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    main()
