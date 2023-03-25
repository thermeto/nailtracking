import base64
import time
import pika
import infer_photo
import os


# Function to handle incoming messages
def on_message(channel, method_frame, header_frame, body):
    image_path = body.decode('utf-8')  # Decode the received image path

    # Update the image path according to Dockerfile's file locations
    input_image_path = os.path.join('/input_images', os.path.basename(image_path))

    # Process the image and get the output path
    output_image_path = infer_photo.transparentize_nails(input_image_path)

    # Prepare the modified image as a base64-encoded string
    with open(output_image_path, 'rb') as f:
        modified_image = base64.b64encode(f.read()).decode('utf-8')

    # Send the modified image back to the result queue specified in the reply_to property
    channel.basic_publish(exchange='',
                          routing_key=header_frame.reply_to,
                          properties=pika.BasicProperties(correlation_id=header_frame.correlation_id),
                          body=modified_image)

    # Acknowledge the message so it is removed from the nailtracking_queue
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Declare the input queue (nailtracking_queue)
channel.queue_declare(queue='nailtracking_queue')

# Set up the consumer to listen for messages on the nailtracking_queue and handle them using the on_message function
channel.basic_consume(queue='nailtracking_queue', on_message_callback=on_message)


def start_consuming():
    try:
        print(' [*] Waiting for messages. To exit press CTRL+C')
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
