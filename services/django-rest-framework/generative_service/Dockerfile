# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# (Obsolete) Install PyTorch, torchvision, and torchaudio from PyTorch wheel files
# RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install C compiler and the Python development headers
RUN apt-get update && apt-get install -y build-essential python-dev-is-python3

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose the port uWSGI will listen on
EXPOSE 8000

# Define the command to start the container
CMD uwsgi --http :8000 --module generative_service.wsgi
