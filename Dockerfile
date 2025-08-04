FROM quay.io/centos/centos:stream9

RUN dnf install -y python3.9 python3-pip

WORKDIR /pe-portfolio

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

