FROM python:3.6

RUN mkdir -p /scripts

WORKDIR /scripts

COPY requirements.txt /scripts

RUN pip3 install -r requirements.txt

COPY . /scripts

CMD ["python", "predict.py"]
