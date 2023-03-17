FROM python:3.9-alpine3.16

COPY requirements.txt /tmp/requirements.txt
COPY bot bot

WORKDIR bot

RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

CMD ["python", "main.py"]

EXPOSE 8000
