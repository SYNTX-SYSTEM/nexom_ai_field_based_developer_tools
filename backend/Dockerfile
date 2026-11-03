FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY backend /app/backend
RUN mkdir -p /app/data
ENV PYTHONPATH=/app/backend
CMD ["uvicorn","api.main:app","--host","0.0.0.0","--port","8000"]
