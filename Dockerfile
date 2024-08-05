# Base image for Python application
FROM python:3.12-alpine

# Create a working directory within the container
WORKDIR /app

# Copy requirements.txt file
COPY requirements.txt .

# Install dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY templates ./templates
COPY src ./src

EXPOSE 8000

# Command to run the application (replace "main:app" with your actual entry point)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
