# Python image to use.
#ROM ultralytics/ultralytics:latest-python
FROM python:3.11-bookworm
# Set the working directory to /app



RUN apt update \
    && apt install --no-install-recommends -y python3-pip git zip curl htop libgl1 libglib2.0-0 libpython3-dev gnupg g++ libusb-1.0-0 vim

RUN python3 -m pip install --upgrade pip



RUN mkdir /app

WORKDIR /app

COPY runs/detect/train/weights/best.pt runs/detect/train/weights/best.pt
COPY detector/ detector/
COPY static/ static/
COPY templates/ templates/
COPY requirements.txt/ .
COPY app.py .
# copy the requirements file used for dependencies


#RUN bash ./setup.sh
# Install any needed packages specified in requirements.txt
RUN pip install  -r requirements.txt

# Copy the rest of the working directory contents into the container at /app


# Run app.py when the container launches
ENTRYPOINT ["python", "app.py"]
