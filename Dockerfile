# Use an official Python runtime as a parent image
FROM python:3.9-slim

# --- NEW COMMANDS ---
# Install the missing system library (libgomp.so.1)
# This is needed for scikit-learn/pycaret
RUN apt-get update && apt-get install -y libgomp1
# --- END NEW COMMANDS ---

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
# We use --no-cache-dir to keep the image size small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code (app.py, model, templates)
COPY . .

# Expose the port the app will run on (matches our app.py)
EXPOSE 7860

# Define the command to run the application
# This will execute: python app.py
CMD ["python", "app.py"]