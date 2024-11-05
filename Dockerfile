FROM python:3.8

WORKDIR /pythonProject2

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

