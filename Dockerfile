FROM python:3.10-slim-buster

# Set working directory
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the port the application will listen on
EXPOSE 8080

# Command to run the application using Uvicorn
CMD ["uvicorn", "rest_api.app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]