# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Make port 8443 available to the world outside this container
EXPOSE 8443

# Define environment variable
ENV TELEGRAM_TOKEN=your-telegram-bot-token

# Run the bot
CMD ["python", "./main.py"]