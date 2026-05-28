FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p static/uploads

EXPOSE 7860

ENV FLASK_APP=app.py

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]