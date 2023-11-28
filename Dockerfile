FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

COPY . /app

CMD ["uvicorn", "service.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
