# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory within the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the entire app directory into the container at /app
COPY . /app

# Expose port 8000 for the Flask app to listen on
EXPOSE 8000

# Run Gunicorn to serve the Flask app
CMD ["gunicorn", "-c", "gunicorn-config.py", "server:app"]
#CMD ["python", "server.py"]