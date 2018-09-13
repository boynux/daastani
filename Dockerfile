FROM resin/rpi-raspbian:stretch

RUN groupadd -r daastani && useradd -r -m -g daastani daastani
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
       python \
       python-pip \
       python-pygame \
       rpi.gpio

WORKDIR /home/daastani

RUN apt-get install --no-install-recommends -y \
       build-essential \
       libpython-dev \
       python-setuptools \
       git \
    && git clone https://github.com/lthiery/SPI-Py \
    && cd SPI-Py \
    && python setup.py install \
    && rm -rf SPI-Py \
    && apt-get remove -y build-essential libpython-dev git python-setuptools \
    && apt-get autoremove \
    && apt-get clean

COPY . /home/daastani
RUN chown daastani:daastani -R /home/daastani

USER daastani
RUN pip install -r requirements.txt

ENV AWS_IOT_CREDS_URL=aws-url
ENV CERT_PEM_PATH=cert-key-path
ENV CERT_PEM_PATH=cert-key-path

CMD ["python", "app.py"]

