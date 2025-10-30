FROM python:3.10-slim


WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN mkdir -p static/uploads models


EXPOSE 8080


ENV PORT=8080
ENV TF_ENABLE_ONEDNN_OPTS=0


CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "--timeout", "0", "app:app"]