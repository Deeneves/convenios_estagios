FROM node:20-slim AS tailwind

WORKDIR /app

COPY package.json package-lock.json tailwind.config.js ./
COPY templates ./templates
COPY apps ./apps
COPY static/css/tailwind.input.css ./static/css/tailwind.input.css

RUN npm ci \
    && npm run build:css

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY --from=tailwind /app/static/css/tailwind.css /app/static/css/tailwind.css

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
