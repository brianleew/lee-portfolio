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

# Run python import.py script
CMD ["python3", "import.py", "-c"]