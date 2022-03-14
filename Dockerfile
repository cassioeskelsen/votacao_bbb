FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . .

#CMD ["gunicorn", "app.main:app", "--workers", "50", "--log-level", "error", "--bind", "0.0.0.0:80", "--worker-class", "sanic.worker.GunicornWorker", ">","/dev/null"]
CMD ["sanic", "app.main:app", "--host=0.0.0.0", "--port=80", "--workers=30"]