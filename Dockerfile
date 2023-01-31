FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Flask application files to the container
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port 5000 to allow incoming traffic to the container
EXPOSE 5000

# Set the command to run when the container starts
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]