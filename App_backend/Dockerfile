
# Base Image

FROM python:3.12-slim

# Environment

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working Directory

WORKDIR /app

# Install Dependencies

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy Project

COPY . .

# Expose Port

EXPOSE 8000

# Start FastAPI

CMD [
    "uvicorn",
    "app:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
]