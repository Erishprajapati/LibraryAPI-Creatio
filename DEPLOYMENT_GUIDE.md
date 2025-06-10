# Deployment Guide

## Backend Deployment (Railway)

### Step 1: Deploy Backend to Railway

1. **Go to [Railway.app](https://railway.app)**
2. **Sign up/Login** with your GitHub account
3. **Click "New Project"** → "Deploy from GitHub repo"
4. **Select your repository**
5. **Railway will automatically detect** it's a Python project
6. **Add Environment Variables**:
   - `DATABASE_URL` = Your PostgreSQL connection string
   - `SECRET_KEY` = A random secret key for JWT tokens

### Step 2: Get Your Backend URL

After deployment, Railway will give you a URL like:
`https://your-app-name.railway.app`

## Frontend Deployment (Vercel)

### Step 1: Update Frontend Configuration

1. **Go to your Vercel dashboard**
2. **Select your project**
3. **Go to Settings** → **Environment Variables**
4. **Add**:
   - `VITE_API_URL` = `https://your-app-name.railway.app`

### Step 2: Redeploy Frontend

1. **Go to Deployments tab**
2. **Click "Redeploy"** on the latest deployment

## Alternative Backend Deployment Options

### Option 1: Render
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Option 2: Heroku
1. Go to [heroku.com](https://heroku.com)
2. Create new app
3. Connect GitHub repo
4. Add PostgreSQL addon
5. Deploy

## Database Setup

### For Railway/Render/Heroku:
- Use the built-in PostgreSQL service
- The `DATABASE_URL` will be automatically provided

### For Local Development:
- Keep using your local PostgreSQL database

## Troubleshooting

### Common Issues:

1. **"Not Found" Error**: Backend not deployed or wrong API URL
2. **Database Connection Error**: Check `DATABASE_URL` environment variable
3. **CORS Error**: Update backend CORS origins with your Vercel domain

### Check Backend Health:
Visit: `https://your-backend-url.railway.app/` - should show FastAPI docs

### Check Frontend:
Visit: `https://your-app.vercel.app` - should show your React app

## Environment Variables Summary

### Backend (Railway/Render/Heroku):
```
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=your-secret-key-here
```

### Frontend (Vercel):
```
VITE_API_URL=https://your-backend-url.railway.app
``` 