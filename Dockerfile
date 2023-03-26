FROM thermeto/garnify:tf0.0.1

RUN apt-get update && apt-get install -y libgl1

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

RUN apt-get update && \
    apt-get install -y \
        libxkbcommon-x11-0 \
        libxcb1 \
        libxcb-render0 \
        libxcb-shm0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-shape0 \
        libxcb-sync1 \
        libxcb-xfixes0 \
        libxcb-xinerama0 \
        libxcb-xkb1 \
        libx11-xcb1 \
        libxcb-glx0 \
        libxcb-xinerama0-dev \
        libxcb-util1 \
        libsm6 \
        xvfb

ENV QT_QPA_PLATFORM_PLUGIN_PATH /usr/local/lib/python3.8/dist-packages/cv2/qt/plugins/platforms
ENV QT_DEBUG_PLUGINS 1

COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]