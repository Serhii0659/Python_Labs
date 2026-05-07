FROM python:3.12-slim

WORKDIR /kovalenko

COPY requirements.txt .
COPY task1.py .
COPY 10_kovalenko.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["/bin/bash"]