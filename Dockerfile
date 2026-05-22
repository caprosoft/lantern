FROM python:3.11

WORKDIR /app
COPY . .

RUN apt-get update && apt-get upgrade -y && apt-get install -y nmap
RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]