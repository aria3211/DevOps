FROM python:3.11-slim


WORKDIR /app


COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY app/ ./


ENV PYTHONUNBUFFERED=1


EXPOSE 8000


# healthcheck: curl http://localhost:8000/healthz should return 200
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
CMD curl -f http://localhost:8000/healthz || exit 1


CMD ["python", "app.py"]
