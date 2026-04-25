# Use Python version
FROM python:3.13-slim

# Enviroment
ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Working directory
WORKDIR /app

# Update system
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    libgobject-2.0-0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libcairo2 \
    libffi-dev \
    shared-mime-info \
    locales \
    && locale-gen es_ES.UTF-8 \
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
