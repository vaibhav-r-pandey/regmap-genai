#!/bin/bash

echo "🚀 Deploying Share WebUI to HICP..."

# Apply the deployment
kubectl apply -f hicp-deploy.yaml

# Wait for deployments
echo "⏳ Waiting for deployments..."
kubectl wait --for=condition=available --timeout=600s deployment/share-webui-frontend
kubectl wait --for=condition=available --timeout=600s deployment/share-webui-backend
kubectl wait --for=condition=available --timeout=600s deployment/mongodb

echo "✅ Deployment completed!"
echo "📝 Check status: kubectl get pods"
echo "🌐 Port forward: kubectl port-forward svc/share-webui-frontend 3000:80"