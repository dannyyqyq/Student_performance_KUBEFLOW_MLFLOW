FROM python:3.13-slim
WORKDIR /app

COPY components/model-training/train.py /app/train.py
RUN pip install --no-cache-dir pandas scikit-learn loguru joblib

ENTRYPOINT ["python", "/app/train.py"]
