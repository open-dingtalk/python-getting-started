FROM python:3.10-alpine

WORKDIR /work
 
ADD . .
COPY ./settings.example.py /work/settings.py

RUN apk add build-base libffi libffi-dev \
    && pip install -r requirements.txt

EXPOSE 7001

CMD ["python", "./app.py"]
