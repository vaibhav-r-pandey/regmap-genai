# Share WebUI - Diff Checker Application

A full-stack web application for comparing text files with a React frontend and Node.js backend, ready for HICP deployment.

## Architecture

- **Frontend**: React application with nginx
- **Backend**: Node.js/Express API server
- **Database**: MongoDB
- **Deployment**: Docker containers with Kubernetes manifests

## Prerequisites

- Node.js 18+
- Docker and Docker Compose
- MongoDB (for local development)
- kubectl (for Kubernetes deployment)

## Local Development

### Setup Environment

1. Copy environment files:
```bash
cp .env.example .env
cp backend/.env.example backend/.env
```

2. Install dependencies:
```bash
# Frontend
npm install

# Backend
cd backend
npm install
```

### Running with Docker Compose

```bash
docker-compose up --build
```

Access the application at http://localhost

### Running Locally

1. Start MongoDB:
```bash
mongod
```

2. Start backend:
```bash
cd backend
npm run dev
```

3. Start frontend:
```bash
npm start
```

Access the application at http://localhost:3000

## Production Deployment

### Docker Images

Build production images:
```bash
# Frontend
docker build -t share-webui-frontend .

# Backend
docker build -t share-webui-backend ./backend
```

### Kubernetes Deployment

1. Apply Kubernetes manifests:
```bash
kubectl apply -f k8s/
```

2. Update image references in k8s/*.yaml files with your registry URLs

### HICP Deployment

1. Configure GitHub secrets:
   - `REGISTRY_URL`: Container registry URL
   - `REGISTRY_USERNAME`: Registry username
   - `REGISTRY_PASSWORD`: Registry password

2. Push to main branch to trigger deployment

## Environment Variables

### Frontend (.env)
- `REACT_APP_API_URL`: Backend API URL

### Backend (backend/.env)
- `NODE_ENV`: Environment (development/production)
- `PORT`: Server port (default: 5000)
- `MONGO_URI`: MongoDB connection string
- `FRONTEND_URL`: Frontend URL for CORS

## API Endpoints

- `GET /health`: Health check
- `POST /api/files`: Save comparison data

## Features

- Text comparison with line-by-line diff
- File upload support
- Synchronized scrolling
- Save comparison results
- Responsive design

## Scripts

### Frontend
- `npm start`: Development server
- `npm build`: Production build
- `npm test`: Run tests

### Backend
- `npm start`: Production server
- `npm run dev`: Development server with nodemon

## Monitoring

- Health check endpoint: `/health`
- Kubernetes probes configured for liveness and readiness
- Resource limits defined in manifests

## GitHub Setup

1. Initialize git repository:
```bash
git init
git add .
git commit -m "Initial commit - HICP ready deployment"
```

2. Create GitHub repository and push:
```bash
git remote add origin https://github.com/yourusername/share-webui.git
git branch -M main
git push -u origin main
```