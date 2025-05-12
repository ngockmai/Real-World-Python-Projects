# Use an official Python runtime as a parent image
FROM python:slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (if any)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . /app/

# Expose the port the app runs on (should match docker-compose.yml)
EXPOSE 8000

# Run the Django development server (or gunicorn for production)
# Adjust the command based on your project structure if manage.py is not in the root
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
