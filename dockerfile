# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the necessary tools
RUN pip install --upgrade pip setuptools wheel twine

# Build the distribution packages
RUN python setup.py sdist bdist_wheel

# Upload the package to PyPI
CMD ["sh", "-c", "twine upload dist/* -u  -p "]