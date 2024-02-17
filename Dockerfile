FROM debian:bookworm

RUN apt-get update && apt-get install -y wget

RUN t=$(mktemp) && \
    wget 'https://dist.1-2.dev/imei.sh' -qO "$t" && \
    bash "$t" && \
    rm "$t"

RUN apt-get install -y python3.11 python3.11-venv xvfb && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN python3 -m venv /venv

RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "/venv/bin/python3", "main.py"]
