# Share WebUI - Git Import Deployment

A React diff checker application with Node.js backend, ready for HICP git import.

## HICP Deployment

### 1. Import from Git
1. Go to HICP **Applications** → **Import from Git**
2. Repository: `https://github.com/vaibhav-r-pandey/regmap-genai.git`
3. Context: `share_webui`
4. Build: Node.js
5. Deploy

### 2. Local Development
```bash
git clone https://github.com/vaibhav-r-pandey/regmap-genai.git
cd regmap-genai/share_webui
docker compose up --build
```

### 3. Access
- HICP: Use generated route
- Local: http://localhost:3000

## What's Included
- **Frontend**: React app (port 3000)
- **Backend**: Node.js API (port 5000)  
- **Database**: MongoDB (port 27017)

## Environment Variables
- `REACT_APP_API_URL`: Backend API URL
- `NODE_ENV`: Environment mode
- `MONGO_URI`: MongoDB connection string

## Development
```bash
# Frontend
npm install
npm start

# Backend
cd backend
npm install
npm run dev
```