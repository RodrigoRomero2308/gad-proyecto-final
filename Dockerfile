# Build with: docker build -t chirplyfy-server .
FROM python:3.8.10

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "app.py" ]