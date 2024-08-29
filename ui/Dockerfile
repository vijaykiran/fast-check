FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.lock ./
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

COPY src .
# Expose the port the app runs on
EXPOSE 80

# Run the app with the Litestar CLI
CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "80"]
