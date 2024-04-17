# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./requirements.txt /app/
# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt


COPY . /app/


RUN python3 manage.py migrate

# Expose port 8000 for the Django development server
EXPOSE 8000