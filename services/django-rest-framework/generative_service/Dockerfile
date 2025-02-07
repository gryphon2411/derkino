# Use an official Python runtime as an image builder
FROM python:3.10 AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install build tools (only needed for building)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential python-dev-is-python3

# Copy requirements.txt first for caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/


# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install libxml2
RUN apt-get update && apt-get install -y --no-install-recommends libxml2 libxml2-dev

# Copy app files from builder stage
COPY --from=builder /app /app

# Copy the uwsgi executable from builder stage
COPY --from=builder /usr/local/bin/uwsgi /usr/local/bin/

# Copy installed Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

# Expose the port uWSGI will listen on
EXPOSE 8000

# Define the command to start the container (using JSON array format)
CMD ["uwsgi", "--http", ":8000", "--module", "generative_service.wsgi"]