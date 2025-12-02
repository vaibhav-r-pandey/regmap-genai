# HICP Server Deployment

## Steps:

### 1. Push Code to GitHub
```bash
git push origin main
```

### 2. Deploy to HICP (Deploy in Order)
**Step 1: Deploy Application**
1. Go to **Workloads** → **Deployments**
2. Click **"Create from YAML"**
3. Copy content from `hicp-deployment.yaml`
4. Paste and click **"Create"**

**Step 2: Create Service**
1. Go to **Services**
2. Click **"Create from YAML"**
3. Copy content from `hicp-service.yaml`
4. Paste and click **"Create"**

### 3. Access Application
- Go to **Services** → **share-webui-service**
- Use external IP on port 3000

## What This Does:
- Clones your GitHub repo
- Builds React app
- Runs frontend on port 3000
- Runs backend on port 5000
- Includes MongoDB database
- All in one pod for simplicity

## Troubleshooting:
- Check pod logs if deployment fails
- Ensure GitHub repo is public
- Wait for build to complete (may take 2-3 minutes)