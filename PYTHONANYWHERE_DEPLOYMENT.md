# PythonAnywhere Deployment Guide

## Step 1: Upload Your Code

### Option A: Using Git (Recommended)
1. Go to PythonAnywhere dashboard
2. Click on "Files" tab
3. Open a Bash console by clicking "Bash" or "New Console"
4. Navigate to your home directory and clone your repository:
   ```bash
   cd ~
   git clone https://github.com/yourusername/your-repo-name.git library-api
   cd library-api
   ```

### Option B: Manual Upload
1. Go to "Files" tab in PythonAnywhere
2. Create a new directory called `library-api`
3. Upload your files one by one or zip and upload:
   - `main.py`
   - `start.py`
   - `models.py`
   - `schemas.py`
   - `database.py`
   - `hashing.py`
   - `requirements.txt`
   - `recreate_tables.py`
   - `add_books_back.py`

## Step 2: Set Up Virtual Environment

### Create Virtual Environment
1. Open a Bash console in PythonAnywhere
2. Navigate to your project directory:
   ```bash
   cd ~/library-api
   ```
3. Create a virtual environment:
   ```bash
   python3.9 -m venv venv
   ```
4. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

### Install Dependencies
1. Make sure you're in the virtual environment (you should see `(venv)` in your prompt)
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. If you encounter any issues, install packages individually:
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary python-multipart python-jose[cryptography] passlib[bcrypt]
   ```

## Step 3: Configure Database

### Option A: Use PostgreSQL (Recommended for production)
1. In PythonAnywhere dashboard, go to "Databases" tab
2. Create a new PostgreSQL database
3. Note down the database credentials
4. Update your `database.py` file with the new connection string

### Option B: Use SQLite (For testing)
1. SQLite will work out of the box
2. Make sure `library.db` file is uploaded to your project directory

## Step 4: Set Up Web App

### Create Web App
1. Go to "Web" tab in PythonAnywhere dashboard
2. Click "Add a new web app"
3. Choose "Manual configuration" (not Django)
4. Select Python version 3.9
5. Set the source code directory to `/home/yourusername/library-api`

### Configure WSGI File
1. Click on the WSGI configuration file link
2. Replace the content with:
   ```python
   import sys
   import os
   
   # Add your project directory to Python path
   path = '/home/yourusername/library-api'
   if path not in sys.path:
       sys.path.append(path)
   
   # Activate virtual environment
   activate_this = '/home/yourusername/library-api/venv/bin/activate_this.py'
   with open(activate_this) as file_:
       exec(file_.read(), dict(__file__=activate_this))
   
   # Import your FastAPI app
   from main import app
   
   # For WSGI compatibility
   from fastapi.middleware.wsgi import WSGIMiddleware
   from fastapi.responses import JSONResponse
   
   # Create WSGI app
   def application(environ, start_response):
       return app(environ, start_response)
   ```

### Alternative: Use ASGI with Uvicorn
1. In the WSGI file, use this simpler configuration:
   ```python
   import sys
   import os
   
   # Add your project directory to Python path
   path = '/home/yourusername/library-api'
   if path not in sys.path:
       sys.path.append(path)
   
   # Import your FastAPI app
   from main import app
   
   # For WSGI compatibility
   from fastapi.middleware.wsgi import WSGIMiddleware
   
   # Create WSGI app
   application = WSGIMiddleware(app)
   ```

## Step 5: Initialize Database

### Run Database Setup
1. Open a Bash console
2. Navigate to your project and activate virtual environment:
   ```bash
   cd ~/library-api
   source venv/bin/activate
   ```
3. Run the database setup:
   ```bash
   python recreate_tables.py
   ```
4. Add sample books:
   ```bash
   python add_books_back.py
   ```

## Step 6: Configure Environment Variables

### Set Environment Variables
1. In your PythonAnywhere dashboard, go to "Web" tab
2. Click on your web app
3. Scroll down to "Environment variables"
4. Add these variables:
   - `DATABASE_URL`: Your database connection string
   - `SECRET_KEY`: A random secret key for JWT tokens
   - `ENVIRONMENT`: `production`

## Step 7: Reload and Test

### Reload Web App
1. Go to "Web" tab
2. Click "Reload" button
3. Wait for the reload to complete

### Test Your API
1. Your API will be available at: `https://yourusername.pythonanywhere.com`
2. Test the endpoints:
   - `https://yourusername.pythonanywhere.com/docs` (FastAPI docs)
   - `https://yourusername.pythonanywhere.com/books` (Get books)
   - `https://yourusername.pythonanywhere.com/register` (Register user)

## Step 8: Troubleshooting

### Common Issues and Solutions

1. **Import Errors**: Make sure all files are uploaded and virtual environment is activated
2. **Database Connection**: Check your database credentials and connection string
3. **Port Issues**: PythonAnywhere handles ports automatically, don't specify port in your code
4. **CORS Issues**: Update CORS settings in `main.py` to allow your frontend domain

### Check Logs
1. Go to "Web" tab
2. Click on "Error log" to see any errors
3. Check "Server log" for general information

## Step 9: Frontend Deployment (Optional)

### Deploy Frontend Separately
1. Build your React frontend:
   ```bash
   cd frontend
   npm run build
   ```
2. Upload the `build` folder to a static hosting service (Netlify, Vercel, etc.)
3. Update CORS settings in your backend to allow the frontend domain

## Important Notes

- PythonAnywhere free accounts have limitations on external network access
- For production use, consider upgrading to a paid account
- Make sure to keep your secret keys secure
- Regularly backup your database
- Monitor your application logs for any issues

## Quick Commands Reference

```bash
# Navigate to project
cd ~/library-api

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database setup
python recreate_tables.py

# Add sample data
python add_books_back.py

# Test locally (if needed)
python start.py
``` 