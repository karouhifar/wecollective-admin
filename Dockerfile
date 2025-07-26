# 1. Base image
FROM python:3.10-slim


# 1.1. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 2. Set workdir
WORKDIR /app

# 3. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy source
COPY . .
# 5. Collect static files
RUN python manage.py collectstatic --noinput
# 6. Expose & run
EXPOSE 8000
CMD ["gunicorn", "wecollectiveadmin.wsgi:application", "--bind", "0.0.0.0:8000"]
