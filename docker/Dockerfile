# Use an official Python runtime as a parent image
FROM python:3.6.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Used for caching
RUN pip install keras
RUN pip install tensorflow
RUN pip install gym
RUN pip install gym[atari]

#ViZDoom install 
RUN apt-get update

RUN apt-get -y install build-essential zlib1g-dev libsdl2-dev libjpeg-dev \
nasm tar libbz2-dev libgtk2.0-dev cmake git libfluidsynth-dev libgme-dev \
libopenal-dev timidity libwildmidi-dev unzip

RUN apt-get -y install libboost-all-dev

RUN pip install vizdoom

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "full_test.py"]
