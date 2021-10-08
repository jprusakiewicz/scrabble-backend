FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN apt-get update
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 80
ARG LOG_LEVEL=10
COPY ./app /app
ENV PYTHONPATH=/
ENV EXPORT_RESULTS_URL="https://backend-dev.capgemini.enl-projects.com"
