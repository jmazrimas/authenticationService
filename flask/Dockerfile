# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8090 available to the world outside this container
EXPOSE 8090

# Define environment variable
ARG google_oauth_client_id
ARG google_oauth_secret
ARG auth_svc_db_name
ARG auth_svc_db_user
ARG auth_svc_db_pass

ENV GOOGLE_OAUTH_CLIENT_ID=$google_oauth_client_id
ENV GOOGLE_OAUTH_SECRET=$google_oauth_secret
ENV AUTH_SVC_DB_NAME=$auth_svc_db_name
ENV AUTH_SVC_DB_USER=$auth_svc_db_user
ENV AUTH_SVC_DB_PASS=$auth_svc_db_pass

# Run app.py when the container launches
CMD ["python", "app.py"]