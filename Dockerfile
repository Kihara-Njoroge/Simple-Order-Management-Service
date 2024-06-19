# ---- Build Stage ----
FROM python:3.10-slim AS build

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

# Make entrypoint script executable
RUN sed -i 's/\r$//' entrypoint.sh || true && chmod +x entrypoint.sh

# ---- Production Stage ----
# Use a minimal Python image for production
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory in the container
WORKDIR /app

# Copy built files from the build stage
COPY --from=build /app /app

# Specify the command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
