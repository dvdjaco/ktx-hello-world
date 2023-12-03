# Dockerfile
FROM python:3.9-slim
WORKDIR /hello_world
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
ENV IMAGE_TAG latest
COPY . .
CMD ["python", "hello_world.py"]
