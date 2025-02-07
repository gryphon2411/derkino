# Use an official Python runtime as an image builder
FROM python:3.10 AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create non-root user 'appuser' (UID 1000) and group for security
RUN groupadd -r appuser && useradd -r -g appuser -u 1000 appuser

# Set work directory
WORKDIR /app

# Install build tools (as root, temporarily)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential python-dev-is-python3

# Copy requirements.txt first for caching
COPY requirements.txt ./

# Switch to non-root user
USER appuser

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create the same non-root user and group in the final image
RUN groupadd -r appuser && useradd -r -g appuser -u 1000 appuser

# Set work directory
WORKDIR /app

# Copy app files from the builder stage
COPY --from=builder /app /app
# Copy installed Python packages from the builder stage (chown to ensure correct ownership)
COPY --from=builder --chown=appuser:appuser /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

# Switch to non-root user
USER appuser

# Expose the port uWSGI will listen on
EXPOSE 8000

# Define the command to start the container (using JSON array format)
CMD ["uwsgi", "--http", ":8000", "--module", "generative_service.wsgi"]