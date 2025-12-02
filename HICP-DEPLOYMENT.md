# HICP Web UI Deployment Guide

## Steps to Deploy via HICP Web Interface:

### 1. Access HICP Dashboard
- Login to your HICP web interface
- Navigate to **Workloads** → **Deployments**

### 2. Create New Deployment
- Click **"Create"** or **"+"** button
- Select **"Create from YAML"**

### 3. Copy and Paste YAML
- Copy the entire content from `hicp-web-deploy.yaml`
- Paste into the YAML editor
- Click **"Create"** or **"Apply"**

### 4. Monitor Deployment
- Go to **Workloads** → **Pods**
- Wait for pod status to show **"Running"**
- Check logs if any issues occur

### 5. Access Application
- Go to **Services** → **share-webui-service**
- Use the external IP/URL provided
- Application will be available on port 80

## Troubleshooting:
- If pods fail, check **Events** tab
- View pod logs for error details
- Ensure git repository is accessible

## Files Needed:
- `hicp-web-deploy.yaml` - Main deployment file
- GitHub repository must be public or accessible

## What This Deploys:
- Frontend (React app on port 3000)
- Backend (Node.js API on port 5000) 
- MongoDB (Database on port 27017)
- LoadBalancer service for external access