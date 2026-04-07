# Use Python version
FROM python:3.13-slim

# Enviroment
ENV \
    PATH=/app/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Update system
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies file
COPY requirements.txt .

# Install dependecies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the project to the container
COPY . .

# Entrypoint permissions
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Run server
CMD ["/app/entrypoint.sh"]
