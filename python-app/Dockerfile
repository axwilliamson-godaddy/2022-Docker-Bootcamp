# Use the small python image, no need for fancy add-ons
FROM python:3.8-slim-buster

# Use /app as our working directory
WORKDIR /app

# Copy our requirements
COPY requirements.txt requirements.txt

# Install our requirements
RUN pip3 install -r requirements.txt

# Copy the rest of our project
COPY . .

# Run our app
ENTRYPOINT [ "python3", "redis_client.py"]