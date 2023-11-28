# Stage 1: Build the application
FROM alpine:3.14

WORKDIR /app

COPY . .

# Install Python and other dependencies
RUN apk update && \
    apk add --no-cache python3 py3-pip libpq gcc python3-dev musl-dev

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Install application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Set the environment variable
ENV FLASK_APP app.py

# Run the application
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
