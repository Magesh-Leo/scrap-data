FROM python:3.8-slim
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY ./app /app
CMD [ "uvicorn", "app.main:app", "--host","0.0.0.0","--port", "8000" ]