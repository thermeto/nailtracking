# Use the official TensorFlow GPU image as the base image
FROM tensorflow/tensorflow:2.7.0-gpu

# Set the working directory
WORKDIR /tensorflow

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub

# Install necessary system packages
RUN apt-get update && \
    apt-get install -y \
    git \
    protobuf-compiler \
    python3-tk

# Install Python packages
RUN pip install --no-cache-dir \
    cython \
    contextlib2 \
    lxml \
    jupyter \
    matplotlib \
    pillow \
    pycocotools \
    opencv-python-headless

# Clone the TensorFlow models repository
RUN git clone https://github.com/tensorflow/models.git

# Compile protobuf files and install the object_detection package
RUN cd models/research && \
    protoc object_detection/protos/*.proto --python_out=. && \
    cp object_detection/packages/tf2/setup.py . && \
    python -m pip install .

# Set the PYTHONPATH environment variable for the object_detection directory
ENV PYTHONPATH=$PYTHONPATH:/tensorflow/models/research:/tensorflow/models/research/slim

# Expose Jupyter Notebook port
EXPOSE 8888

# Start Jupyter Notebook
CMD ["jupyter", "notebook", "--allow-root", "--ip=0.0.0.0", "--no-browser", "--NotebookApp.token=''"]
