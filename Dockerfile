FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY load_gen.py .
ENV TARGET_URL=http://51.21.255.185:5000
ENV REQUESTS_PER_SECOND=20
ENV DURATION_SEC=130
CMD ["python", "load_gen.py"]