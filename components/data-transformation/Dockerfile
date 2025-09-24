FROM python:3.13-slim
WORKDIR /app

COPY components/data-transformation/transform.py /app/transform.py
RUN pip install --no-cache-dir pandas scikit-learn loguru

ENTRYPOINT ["python", "/app/transform.py"]
