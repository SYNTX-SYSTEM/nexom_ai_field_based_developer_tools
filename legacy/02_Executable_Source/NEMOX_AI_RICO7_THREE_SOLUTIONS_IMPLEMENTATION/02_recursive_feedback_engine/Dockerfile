FROM python:3.12-slim
WORKDIR /app
COPY shared /app
COPY 02_recursive_feedback_engine/backend /app/backend
COPY 02_recursive_feedback_engine/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/app
CMD ["uvicorn","backend.main:app","--host","0.0.0.0","--port","8012"]
