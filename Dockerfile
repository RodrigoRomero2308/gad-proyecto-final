# Build with: docker build -t chirplyfy-server .
FROM python:3.8.10-alpine

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "app.py" ]