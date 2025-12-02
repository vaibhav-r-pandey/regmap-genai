# HICP Git Import Deployment

## Steps:

### 1. Push Code to GitHub
```bash
git push origin main
```

### 2. Import from Git in HICP
1. Go to **Applications** or **Workloads**
2. Click **"Import from Git"** or **"Deploy from Git"**
3. Enter repository URL: `https://github.com/vaibhav-r-pandey/regmap-genai.git`
4. Set context path: `share_webui`
5. Select **Node.js** as build strategy
6. Click **"Create"** or **"Deploy"**

### 3. Configure Ports (if needed)
- Frontend: Port 3000
- Backend: Port 5000

### 4. Access Application
- Use the generated route/URL
- Application will be available once build completes

## What HICP Will Do:
- Clone your GitHub repository
- Detect Node.js application
- Build React frontend
- Run the application
- Create routes automatically

## Build Time:
- Initial deployment: 3-5 minutes
- Subsequent updates: Push to GitHub triggers rebuild