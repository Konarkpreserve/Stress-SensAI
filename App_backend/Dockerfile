
# Base Image

FROM python:3.12-slim

# Environment

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working Directory

WORKDIR /app

# Install Linux Dependencies

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Dependencies

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy Project

COPY . .

# Make startup script executable

RUN chmod +x start.sh

# Expose Port

EXPOSE 8000

# Start FastAPI

CMD ["./start.sh"]