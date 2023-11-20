# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /time_tracker

# Copy the application requirements file to the container
COPY ./requirements.txt /time_tracker/requirements.txt

# Install any dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application code to the container
COPY . /time_tracker

# Expose the port that the application will run on
EXPOSE 8000

# Command to run your application
CMD ["gunicorn", "time_tracker.wsgi:application", "--bind", "0.0.0.0:8000"]
