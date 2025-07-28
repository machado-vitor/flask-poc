FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose the port the app runs on
EXPOSE 5001

# Run the application
CMD ["python", "app.py"]
