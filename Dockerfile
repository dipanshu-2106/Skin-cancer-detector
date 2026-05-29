FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

<<<<<<< HEAD
EXPOSE 7860

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--timeout", "120", "app:app"]
=======
RUN mkdir -p static/uploads

EXPOSE 7860

ENV FLASK_APP=app.py

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
>>>>>>> dcd74f296eb1d9918468141d946f6c6e8ee433a1
