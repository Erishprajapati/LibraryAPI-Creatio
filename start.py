import uvicorn
import os
import sys

if __name__ == "__main__":
    # Debug environment variables
    print("Environment variables:")
    print(f"PORT: {os.environ.get('PORT', 'Not set')}")
    print(f"DATABASE_URL: {'Set' if os.environ.get('DATABASE_URL') else 'Not set'}")
    print(f"ENVIRONMENT: {os.environ.get('ENVIRONMENT', 'Not set')}")
    
    try:
        port = int(os.environ.get("PORT", 8000))
        print(f"Starting server on port {port}")
        
        uvicorn.run(
            "main:app", 
            host="0.0.0.0", 
            port=port, 
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1) 