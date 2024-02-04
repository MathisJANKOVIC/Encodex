FROM python:3.12

WORKDIR /app
COPY . /app

RUN pip install --upgrade --no-cache-dir -r requirements.txt

EXPOSE 80
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
