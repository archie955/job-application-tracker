# Base image
FROM python:3.12-slim

# prevent python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

# working directory
WORKDIR /server
ENV PYTHONPATH=/server

# install system dependencies for psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev netcat-openbsd && rm -rf /var/lib/apt/lists/*

# copy requirements
COPY requirements.txt requirements.txt

# update pip and install deps
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

# finally copy the rest of the app
COPY . .

# expose desired port
EXPOSE 8000

# startup command
CMD ["/usr/local/bin/wait-for-it", "db", "5432", "sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]