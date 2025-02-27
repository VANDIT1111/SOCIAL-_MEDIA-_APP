# Use official Python image
FROM python:3.12.3

# Set working directory inside the container
WORKDIR /hello

# Copy only requirements first (for caching)
COPY requirements.txt .  

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose the port your app runs on
EXPOSE 8080

# Run the application (Direct File Execution)
CMD ["uvicorn", "app.main:fastapi_app", "--host", "0.0.0.0", "--port", "8000"]


