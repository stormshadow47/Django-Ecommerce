FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
    pkg-config \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy only application source needed at runtime (secrets excluded via .dockerignore)
COPY manage.py /app/
COPY ecom_project/ /app/ecom_project/
COPY Users/ /app/Users/
COPY Products/ /app/Products/
COPY cart/ /app/cart/
COPY orders/ /app/orders/
COPY templates/ /app/templates/

# Create logs directory and set permissions
RUN mkdir -p /app/logs && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "ecom_project.wsgi:application", "--bind", "0.0.0.0:8000"]
