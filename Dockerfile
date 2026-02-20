# Use lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependency file first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY scraper.py .

# Create output directory inside container
RUN mkdir -p output

# Default command (state code will be passed at runtime)
ENTRYPOINT ["python", "scraper.py"]
