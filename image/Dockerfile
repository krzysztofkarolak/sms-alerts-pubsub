FROM python:3-alpine
WORKDIR /service
COPY requirements.txt .
RUN apk update && apk add --no-cache g++
RUN pip install -r requirements.txt
COPY . ./
ENTRYPOINT ["python3", "sms.py"]