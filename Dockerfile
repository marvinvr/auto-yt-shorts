FROM python:3.12.1-bookworm

RUN apt remove imagemagick -y

# Download and execute a script
RUN t=$(mktemp) && \
    wget 'https://dist.1-2.dev/imei.sh' -qO "$t" && \
    bash "$t" && \
    rm "$t"

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN chmod -R 777 /app

# Set up Python virtual environment
RUN python3.12 -m venv /venv
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# Use CMD to start cron in the foreground
CMD /venv/bin/python3 /app/main.py
