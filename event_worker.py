import os
import pika
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def callback(ch, method, properties, body):
    # Log each message received
    logging.info(f"Received message: {body.decode()}")
    # Here, you can add more processing logic for each message

def main():
    # Use CloudAMQP URL from your environment variables, if available
    cloudamqp_url = os.getenv('CLOUDAMQP_URL', 'your_default_fallback_connection_string')
    params = pika.URLParameters(cloudamqp_url)

    connection = None
    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        
        # Ensure the queue exists
        channel.queue_declare(queue='anime_updates')

        # Start consuming messages from the queue
        channel.basic_consume(queue='anime_updates', on_message_callback=callback, auto_ack=True)
        logging.info('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Failed to connect to RabbitMQ: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        if connection and not connection.is_closed:
            connection.close()

if __name__ == '__main__':
    main()
