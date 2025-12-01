#!/bin/bash

echo "🚀 Simple HICP Deployment..."

# Build simple images
docker build -f Dockerfile.simple -t share-webui-frontend-simple:latest .
docker build -t share-webui-backend:latest ./backend

# Run with simple compose
docker compose -f docker-compose.simple.yml up --build

echo "✅ Application running on http://localhost:3000"