# Share WebUI - Simple Docker Deployment

A React diff checker application with Node.js backend.

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/vaibhav-r-pandey/regmap-genai.git
cd regmap-genai/share_webui
```

### 2. Run with Docker
```bash
docker compose up --build
```

### 3. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

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