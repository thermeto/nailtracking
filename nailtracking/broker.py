import base64
import time

import numpy as np
import pika
import infer_photo
import os
import cv2

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to handle incoming messages
def on_message(channel, method_frame, header_frame, body):
    logging.info('Received photo')
    output_folder = '/nailtracking_images/output_images'

    image = cv2.imdecode(np.frombuffer(body, np.uint8), cv2.IMREAD_UNCHANGED)

    start_time = time.time()
    # Process the image and get the output path
    output_image = infer_photo.transparentize_nails(image)
    elapsed_time = time.time() - start_time
    logging.info(f"Elapsed time for nailstracking: {elapsed_time:.2f} seconds")

    output_image_path = os.path.join(output_folder, 'output_image.png')
    cv2.imwrite(output_image_path, output_image)
    logging.info(f"Photo {output_image_path} successfully saved")



# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Declare the input queue (nailtracking_queue)
channel.queue_declare(queue='nailtracking_input')

# Set up the consumer to listen for messages on the nailtracking_queue and handle them using the on_message function
channel.basic_consume(queue='nailtracking_input', on_message_callback=on_message)


def start_consuming():
    try:
        print(' [*] Waiting for messages... To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrupted by user, closing...")
        channel.stop_consuming()
        connection.close()
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Restarting consuming process in 5 seconds...")
        time.sleep(5)
        start_consuming()


# Start the consuming process
start_consuming()
