FROM python:3.10-slim

WORKDIR /api

COPY app /api/app
COPY requirements.txt /api/requirements.txt
COPY main.py /api/main.py

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]