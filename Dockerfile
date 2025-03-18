# Use multi-stage build for smaller final image
FROM node:18 AS frontend-build

# Build frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Backend build
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install PM2 globally
RUN npm install -g pm2

# Copy frontend build
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy deployment scripts
COPY deploy.sh .
RUN chmod +x deploy.sh

# Expose ports
EXPOSE 3000 5000

# Start services using PM2
CMD ["./deploy.sh"] 