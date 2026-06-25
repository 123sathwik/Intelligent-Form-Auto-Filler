FROM python:3.10-slim

# Install system utilities and OpenCV dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ml

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy pipeline assets
COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "training/train.py"]
