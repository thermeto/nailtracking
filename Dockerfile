FROM thermeto/garnify:tf0.0.1

# Set the working directory
WORKDIR /nailtracking

# Copy the nailtracking project into the container
COPY . .

# Install RabbitMQ
RUN apt-get update && apt-get install -y rabbitmq-server

# Create input and output image folders
RUN mkdir -p /nailtracking_images/input_images && mkdir -p /nailtracking_images/output_images

# Expose the input and output image folder as a volume
VOLUME /nailtracking_images/input_images
VOLUME /nailtracking_images/output_images

# Install any additional packages required for the project
RUN pip install --no-cache-dir -r requirements.txt

# Run the brocker.py script
CMD ["python", "/nailtracking/consumer.py"]