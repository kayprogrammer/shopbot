FROM python:3.12-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y firefox-esr wget

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Make geckodriver executable
RUN chmod +x ./geckodriver

# Install Python dependencies
RUN pip install -r requirements.txt

# Run your application
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:create_app()"]
