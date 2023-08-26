FROM python:3.8.17-bullseye
RUN apt update && apt install ffmpeg -y
WORKDIR /libraries
RUN git clone https://github.com/tyiannak/pyAudioAnalysis.git
ENV PYTHONPATH=$PYTHONPATH:/libraries
WORKDIR /libraries/pyAudioAnalysis
RUN pip install -r ./requirements.txt
RUN pip install -e .
WORKDIR /code
CMD [ "bash" ]