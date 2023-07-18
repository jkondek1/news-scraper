FROM python:3.10-slim-buster

# Set working directory
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV APP_HOST '0.0.0.0'
ENV APP_PORT 8080
ENV APP_WORKERS 1
ENV DB_HOST 'localhost'
ENV DB_PORT 5432
ENV DB_USER 'postgres'
ENV DB_PASSWORD 'postgres'
ENV DB_NAME 'news'

# Expose the port the application will listen on
EXPOSE $APP_PORT

# Command to run the application using Uvicorn
CMD ["sh","-c","python3 main.py --app_host $APP_HOST --app_port $APP_PORT --app_workers $APP_WORKERS --db_host $DB_HOST --db_port $DB_PORT --db_user $DB_USER --db_password $DB_PASSWORD --db_name $DB_NAME"]