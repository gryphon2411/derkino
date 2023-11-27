# Use the official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /jobs

# Copy requirements.txt to the container
COPY requirements.txt requirements.txt

# Install jobs dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the jobs source code to the container
COPY . .
