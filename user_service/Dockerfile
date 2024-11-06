# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the contents of the user_service directory into the container
COPY . .

# Install dependencies (assuming a requirements.txt is present in the directory)
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5001 for the Flask app
EXPOSE 5001

# Define the command to run the Flask app
CMD ["python", "app.py"]
