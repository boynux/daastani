FROM boynux/daastani:base

COPY . /home/daastani
RUN chown daastani:daastani -R /home/daastani
USER daastani

ENV AWS_IOT_CREDS_URL=aws-url
ENV CERT_PEM_PATH=cert-key-path
ENV CERT_PEM_PATH=cert-key-path

CMD ["python", "app.py"]

