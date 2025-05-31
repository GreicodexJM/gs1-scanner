# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PORT=8080

# Create app directory
WORKDIR /app


# Install Flask for the API
RUN pip install flask flask_cors

# Copy the API code
COPY . /app

# Expose the application port
EXPOSE $PORT

# Run the API
CMD ["python", "/app/api.py"]

