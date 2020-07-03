# Python 3.7
FROM python:3.7

# author
# LABEL maintainer="Javier Guzmán Porras <javier.guzman.porras@gmail.com>"

# Packages that we need
COPY requirements.txt /seada/
COPY seada /seada/

# change the app root directory
WORKDIR /seada

# instruction to be run during image build
RUN pip3 install -r requirements.txt

# execute seada program!
ENTRYPOINT ["python3","seada.py"]

# execute arguments
CMD [""]
