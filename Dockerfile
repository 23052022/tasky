FROM python:3.10.6

WORKDIR /app
COPY ./requirments.txt /app/requirments.txt

RUN pip install -r requirments.txt

COPY . /app
EXPOSE 5000

CMD [ "python", "./app.py" ]
