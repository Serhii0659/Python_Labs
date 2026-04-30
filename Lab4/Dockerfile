# Використовуємо стару версію Python для перевірки gtrans3.py
FROM python:3.12-slim

WORKDIR /kovalenko

# Встановлюємо лише стару версію для цього ізольованого середовища
RUN pip install --no-cache-dir googletrans==3.1.0a0

COPY . .

# Виклик саме другого модуля
CMD ["python", "gtrans3.py"]