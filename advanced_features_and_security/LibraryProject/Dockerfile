# Dockerfile
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["gunicorn", "LibraryProject.wsgi:application", "--bind", "0.0.0.0:8000"]
