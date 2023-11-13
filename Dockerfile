FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app
ADD . /app

RUN pip install -r ./requirements.txt

CMD ["uvicorn", "service.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]