#!/bin/bash

# Share WebUI Deployment Script

set -e

echo "🚀 Starting Share WebUI deployment..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Build Docker images
echo "🔨 Building Docker images..."
docker build -t share-webui-frontend:latest .
docker build -t share-webui-backend:latest ./backend

# Apply Kubernetes manifests
echo "☸️  Applying Kubernetes manifests..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/mongodb.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/mongodb -n share-webui
kubectl wait --for=condition=available --timeout=300s deployment/backend -n share-webui
kubectl wait --for=condition=available --timeout=300s deployment/frontend -n share-webui

echo "✅ Deployment completed successfully!"
echo "📝 Check the status with: kubectl get pods -n share-webui"
echo "🌐 Access the application through the configured ingress or port-forward:"
echo "   kubectl port-forward svc/frontend 8080:80 -n share-webui"