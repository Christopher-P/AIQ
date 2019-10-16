# Use an official Python runtime as a parent image
FROM python:3.6.6

# Set the working directory to /app
WORKDIR /app

# ViZDoom install apps
RUN apt-get update && apt-get install -y \
    build-essential zlib1g-dev libsdl2-dev libjpeg-dev \
    nasm tar libbz2-dev libgtk2.0-dev cmake git libfluidsynth-dev libgme-dev \
    libopenal-dev timidity libwildmidi-dev unzip


RUN apt-get install -y libboost-all-dev

# Install git
RUN apt-get install -y git

# Might be fix for graphics within docker
#RUN apt-get install -y qjackctl

# requirements only into dir
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Download latest AIQ Release
RUN git clone https://github.com/Christopher-P/AIQ.git

# Define environment variable
ENV NAME World

# Move files from examples to above directory
COPY examples/full_test.py /app
COPY examples/sample.yml /app

# Run app.py when the container launches
CMD ["python", "-W ignore","full_test.py"]
