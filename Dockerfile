# Python image to use.
FROM ultralytics/ultralytics:latest-python
#FROM python:3.10-slim-bookworm
# Set the working directory to /app

#ADD https://github.com/ultralytics/assets/releases/download/v0.0.0/Arial.ttf \
#    https://github.com/ultralytics/assets/releases/download/v0.0.0/Arial.Unicode.ttf \
#    /root/.config/Ultralytics/

#RUN apt update \
#    && apt install --no-install-recommends -y python3-pip git zip curl htop libgl1 libglib2.0-0 libpython3-dev gnupg g++ libusb-1.0-0

#UN python3 -m pip install --upgrade pip


WORKDIR /app

COPY . .
# copy the requirements file used for dependencies


RUN bash ./setup.sh
# Install any needed packages specified in requirements.txt
#RUN pip install  -r requirements.txt

# Copy the rest of the working directory contents into the container at /app


# Run app.py when the container launches
ENTRYPOINT ["python3", "app.py"]
