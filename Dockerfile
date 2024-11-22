# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app/ ./app

# Expose the port for the Flask app
EXPOSE 5000

# Run the Flask app
CMD ["python", "app/main.py"]
