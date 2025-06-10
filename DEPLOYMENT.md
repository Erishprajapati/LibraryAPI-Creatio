# Deployment Guide

This guide will help you deploy your Library Management System to production.

## Prerequisites

1. **GitHub Account** - For version control
2. **Vercel Account** - For frontend deployment
3. **Railway Account** (or similar) - For backend deployment
4. **PostgreSQL Database** - For production data

## Step 1: Deploy Backend to Railway

### 1.1 Prepare Backend for Deployment

1. **Update database configuration** for production:
   - Railway will provide a PostgreSQL database URL
   - Update `database.py` to use environment variables

2. **Set environment variables** in Railway:
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `ENVIRONMENT`: Set to "production"

### 1.2 Deploy to Railway

1. Go to [Railway.app](https://railway.app)
2. Create a new project
3. Connect your GitHub repository
4. Add a PostgreSQL database service
5. Deploy your backend code
6. Copy the generated URL (e.g., `https://your-app.railway.app`)

### 1.3 Update CORS Settings

After getting your Railway URL, update the CORS origins in `main.py`:

```python
origins = [
    "https://your-frontend-domain.vercel.app",  # Your Vercel domain
    "https://*.vercel.app",
    "https://your-custom-domain.com"  # If you have a custom domain
]
```

## Step 2: Deploy Frontend to Vercel

### 2.1 Update Frontend Configuration

1. **Update the production API URL** in `frontend/src/config.js`:
   ```javascript
   production: {
     apiUrl: 'https://your-backend-url.railway.app'  // Your Railway URL
   }
   ```

### 2.2 Deploy to Vercel

1. Go to [Vercel.com](https://vercel.com)
2. Create a new project
3. Connect your GitHub repository
4. Set the root directory to `frontend`
5. Configure build settings:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. Deploy

### 2.3 Update Backend CORS

After getting your Vercel URL, update the CORS origins in your backend:

```python
origins = [
    "https://your-app.vercel.app",  # Your actual Vercel domain
    "https://*.vercel.app",
    "https://your-custom-domain.com"
]
```

## Step 3: Environment Variables

### Backend (Railway)
- `DATABASE_URL`: PostgreSQL connection string
- `ENVIRONMENT`: "production"

### Frontend (Vercel)
- No environment variables needed (using config file)

## Step 4: Database Setup

1. **Create tables** in your production database:
   ```bash
   # Run the recreate_tables.py script locally with production DB
   python recreate_tables.py
   ```

2. **Add sample data**:
   ```bash
   # Run the add_books_back.py script
   python add_books_back.py
   ```

## Step 5: Testing

1. **Test the deployed frontend**:
   - Visit your Vercel URL
   - Register a new user
   - Login and test all features

2. **Test API endpoints**:
   - Use tools like Postman or curl
   - Test all CRUD operations

## Troubleshooting

### Common Issues

1. **CORS Errors**:
   - Ensure your backend CORS origins include your Vercel domain
   - Check that the frontend is using the correct backend URL

2. **Database Connection Issues**:
   - Verify your `DATABASE_URL` is correct
   - Ensure your database is accessible from Railway

3. **Build Failures**:
   - Check that all dependencies are in `requirements.txt`
   - Verify the Python version in `runtime.txt`

### Debugging

1. **Check Railway logs** for backend errors
2. **Check Vercel logs** for frontend build issues
3. **Use browser developer tools** to debug API calls

## Security Considerations

1. **Environment Variables**: Never commit sensitive data
2. **CORS**: Only allow necessary origins
3. **Database**: Use strong passwords and SSL connections
4. **HTTPS**: Both Vercel and Railway provide HTTPS by default

## Monitoring

1. **Railway Dashboard**: Monitor backend performance
2. **Vercel Analytics**: Track frontend usage
3. **Database Monitoring**: Monitor database performance

## Updates and Maintenance

1. **Backend Updates**: Push to GitHub, Railway auto-deploys
2. **Frontend Updates**: Push to GitHub, Vercel auto-deploys
3. **Database Migrations**: Use Alembic for schema changes
4. **Backup**: Regular database backups

## Cost Optimization

1. **Railway**: Free tier available, pay for usage
2. **Vercel**: Generous free tier
3. **Database**: Consider managed PostgreSQL services

## Support

- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev 