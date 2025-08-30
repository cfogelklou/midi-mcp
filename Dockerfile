# Dockerfile for MIDI MCP Server

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY src/ /app/src

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV MCP_SERVER_HOST=0.0.0.0
ENV MCP_SERVER_PORT=8000

# Run the application
CMD ["python", "-m", "midi_mcp"]
