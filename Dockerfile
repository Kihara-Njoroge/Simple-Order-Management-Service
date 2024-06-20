# Use the latest Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make entrypoint script executable (if you have one)
RUN sed -i 's/\r$//' entrypoint.sh || true && chmod +x entrypoint.sh

# Specify the command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
