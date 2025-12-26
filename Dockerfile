FROM python:3.10-slim
WORKDIR /app
RUN pip install fastapi uvicorn scikit-learn pandas joblib
COPY api.py .
COPY models/best_model.pkl models/best_model.pkl
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]