# Use the official Python 3.9 image as the base image
FROM python:3.9-slim

# Install system dependencies (e.g., build-essential, libpq-dev for PostgreSQL)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django application code into the container
COPY . /app/

# Copy the entrypoint.sh script into the container
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint.sh script executable
RUN chmod +x /entrypoint.sh

# Expose port 8000 to access the Django app
EXPOSE 8000

# Set the entrypoint to the shell script for migration and app start
ENTRYPOINT ["/entrypoint.sh"]

# Command to run the Django application (after migrations)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
