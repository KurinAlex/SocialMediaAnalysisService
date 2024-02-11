FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install -r docker_requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD ["python", "./Backend/main.py"]