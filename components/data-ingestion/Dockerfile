FROM python:3.13-slim
WORKDIR /app
COPY ingestion.py .
RUN pip install pandas>=2.3.2 pyyaml>=6.0.2 scikit-learn>=1.7.2
CMD ["python", "ingestion.py"]