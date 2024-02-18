FROM debian:bookworm

# Install necessary packages
RUN apt-get update && apt-get install -y wget cron python3.11 python3.11-venv xvfb

# Download and execute a script
RUN t=$(mktemp) && \
    wget 'https://dist.1-2.dev/imei.sh' -qO "$t" && \
    bash "$t" && \
    rm "$t"

# Clean up APT
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Set up Python virtual environment
RUN python3 -m venv /venv
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# Use CMD to start cron in the foreground
CMD /venv/bin/python3 /app/main.py
