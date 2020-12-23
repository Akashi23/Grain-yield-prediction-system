FROM python:3.8-slim

COPY requirements.txt .

RUN apt update

RUN pip install -r requirements.txt

EXPOSE 8000

RUN mkdir app

WORKDIR app

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]