# Railway Deployment Guide

## Step 1: Deploy to Railway

1. **Go to [Railway.app](https://railway.app)**
2. **Sign up/Login** with your GitHub account
3. **Click "New Project"** → **"Deploy from GitHub repo"**
4. **Select your repository**
5. **Railway will automatically detect** it's a Python project

## Step 2: Add Environment Variables

In your Railway project dashboard, go to **Variables** tab and add:

```
DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_random_secret_key_here
ENVIRONMENT=production
```

## Step 3: Get Your Backend URL

After deployment, Railway will give you a URL like:
`https://your-app-name.railway.app`

## Step 4: Update Frontend

1. **Go to your Vercel dashboard**
2. **Select your project**
3. **Go to Settings** → **Environment Variables**
4. **Add**: `VITE_API_URL` = your Railway backend URL
5. **Redeploy** your frontend

## Step 5: Update CORS

In your Railway project, add this environment variable:
```
CORS_ORIGINS=https://your-vercel-domain.vercel.app
```

## Files Created for Deployment

- ✅ `requirements.txt` - Python dependencies
- ✅ `railway.json` - Railway configuration
- ✅ `start.py` - Startup script
- ✅ `nixpacks.toml` - Build configuration
- ✅ `main.py` - Updated for production

## Troubleshooting

If you get "uvicorn: command not found":
1. Make sure `requirements.txt` is in your root directory
2. Check that Railway is using the correct start command: `python start.py`
3. Verify all dependencies are listed in `requirements.txt`

## Your App Should Now Work!

- Frontend: `https://your-app.vercel.app`
- Backend: `https://your-app.railway.app` 