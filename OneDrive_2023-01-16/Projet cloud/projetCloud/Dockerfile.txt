FROM python:3.7-alpine
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN sudo apt-get update && sudo apt-get install ffmpeg libsm6 libxext6  -y
COPY . /app
WORKDIR /app
CMD ["python3","manage.py runserver"]