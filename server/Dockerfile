# Base image
FROM python:3.12-slim

# working directory
WORKDIR /app

# allow for logging
ENV PYTHONBUFFERED=1

# copy requirements
COPY requirements.txt .

# install deps
RUN pip install --no-cache-dir -r requirements.txt

# finally copy the rest of the app
COPY . .

# expose desired port
EXPOSE 8000

# startup command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]