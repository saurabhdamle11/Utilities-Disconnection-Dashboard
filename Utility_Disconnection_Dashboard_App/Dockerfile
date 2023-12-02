# Pull down standard Python Docker base image.
FROM python:3.8.10

# Set working directory.
WORKDIR /usr/src/utility_disconnection_app

# Set environment variables.

# Prevents Python from writing pyc files to disk.
# Python bytecode cache files are only useful on repeated runs of the application.
# Since Docker containers always start fresh, they have no use here.
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents Python from buffering stdout and stderr.
# This just speeds up output to the container logs and ensures nothing is stuck in a buffer.
ENV PYTHONUNBUFFERED 1

# Copy all files in same directory of this Dockerfile to working directory.
COPY . .

# Install application dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# The rest of this file is only used when running this Dockerfile on its own.
# When using Docker compose, these are overridden by the docker-compose.yml settings.

# Open the following port on the container.
EXPOSE 8000

# Start the application.
CMD ["python", "app.py"]
