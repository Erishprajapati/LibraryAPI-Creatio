# Library Management System

A full-stack web application for managing a library system with user authentication, book management, and save functionality.

## Features

- **User Authentication**: Register and login with email/password
- **Book Management**: Browse and view book details
- **Save Books**: Save and unsave books like Instagram
- **User Profiles**: Update user information
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

### Frontend
- **React 19** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **Bootstrap** - UI framework for styling

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Production database
- **Passlib** - Password hashing and verification

## Project Structure

```
├── frontend/                 # React frontend
│   ├── components/          # React components
│   ├── src/                # Source files
│   ├── index.html          # HTML template
│   └── package.json        # Frontend dependencies
├── main.py                 # FastAPI application
├── models.py               # Database models
├── schemas.py              # Pydantic schemas
├── database.py             # Database configuration
├── hashing.py              # Password hashing utilities
├── requirements.txt        # Python dependencies
└── Procfile               # Deployment configuration
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL database

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd library-management-system
   ```

2. **Set up the backend**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Set up database (update database.py with your credentials)
   python recreate_tables.py
   python add_books_back.py
   
   # Start the backend server
   uvicorn main:app --reload
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:5174
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## API Endpoints

### Authentication
- `POST /user` - Register new user
- `POST /home/login` - User login

### Books
- `GET /home` - Get all books
- `GET /home/{book_id}` - Get specific book
- `POST /create` - Create new book (admin)
- `PUT /home/{book_id}` - Update book (admin)
- `DELETE /home/{book_id}` - Delete book (admin)

### User Management
- `PUT /user/update-profile` - Update user profile
- `GET /user/{user_id}` - Get user details

### Saved Books
- `POST /user/save-book` - Save a book
- `GET /user/saved-books` - Get user's saved books
- `DELETE /user/saved-book/{id}` - Remove saved book

## Database Schema

### Users Table
- `id` (Primary Key)
- `name` (String)
- `email` (String, Unique)
- `password` (Hashed String)

### Books Table
- `id` (Primary Key)
- `title` (String)
- `description` (Text)
- `author` (String)
- `published_date` (Integer)

### Saved Books Table
- `id` (Primary Key)
- `user_id` (Foreign Key to Users)
- `book_id` (Foreign Key to Books)

## Development

### Running Tests
```bash
# Backend tests (if implemented)
pytest

# Frontend tests (if implemented)
cd frontend
npm test
```

### Code Style
- Backend: Follow PEP 8
- Frontend: Use ESLint and Prettier

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy

1. **Deploy Backend to Railway**
   - Connect GitHub repository
   - Add PostgreSQL database
   - Set environment variables

2. **Deploy Frontend to Vercel**
   - Connect GitHub repository
   - Set root directory to `frontend`
   - Configure build settings

## Environment Variables

### Backend
- `DATABASE_URL` - PostgreSQL connection string
- `ENVIRONMENT` - "development" or "production"

### Frontend
- No environment variables needed (uses config file)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Create an issue on GitHub
- Check the deployment guide
- Review the API documentation

## Acknowledgments

- FastAPI for the excellent web framework
- React team for the amazing frontend library
- Bootstrap for the UI components
- All contributors and users 