# Original: FROM openhorizon/aarch64-tx2-cudabase

# this is an experimental docker file that should eventually support TX2's onboard camera
#FROM cudabase
FROM w251/cuda:dev-tx2-4.3_b132
# Install package dependencies
RUN apt-get update && apt-get install -y git pkg-config wget
RUN apt-get install -y libgtk2.0-dev pkg-config build-essential cmake libcanberra-gtk-module libcanberra-gtk3-module
RUN apt-get install -y mosquitto mosquitto-clients
RUN apt-get install -y python-pip
# RUN apt-get install -y libgstreamer-plugins-base1.0-0 libgstreamer1.0 libgstreamer-plugins-good1.0-0 libgstreamer-plugins-good1.0-dev

#Install OpenCV. The first commented line is an older version
# RUN apt-get install -y libopencv-dev
WORKDIR /
RUN git clone https://github.com/AlexanderRobles21/OpenCVTX2
WORKDIR /OpenCVTX2
RUN sed -i '72i -D WITH_LIBV4L=ON \\' buildOpenCV.sh
RUN sh buildOpenCV.sh
WORKDIR /root/opencv/build
RUN make 
RUN sudo make install

WORKDIR /
#COPY haarcascade_frontalface_default.xml .
COPY stream_capture.py .
RUN chmod 755 stream_capture.py

RUN pip install paho-mqtt
RUN pip install keyboard
#RUN python face_detection.py


