import React, { useState, useEffect } from 'react';
import { API_BASE_URL } from '../src/config.js';

const Home = ({ userData }) => {
  const [books, setBooks] = useState([]);
  const [loadingBooks, setLoadingBooks] = useState(false);
  const [savedBooks, setSavedBooks] = useState(new Set());
  const [message, setMessage] = useState('');

  const fetchBooks = async () => {
    setLoadingBooks(true);
    try {
      const response = await fetch(`${API_BASE_URL}/home`);
      if (response.ok) {
        const booksData = await response.json();
        setBooks(booksData);
        console.log('Books fetched:', booksData);
      } else {
        console.error('Failed to fetch books');
      }
    } catch (err) {
      console.error('Error fetching books:', err);
    } finally {
      setLoadingBooks(false);
    }
  };

  const fetchSavedBooks = async () => {
    if (!userData?.email) {
      console.log('No user email available, skipping saved books fetch');
      return;
    }
    
    try {
      const response = await fetch(`${API_BASE_URL}/user/saved-books?user_email=${userData.email}`);
      if (response.ok) {
        const savedData = await response.json();
        const savedBookIds = new Set(savedData.map(saved => saved.book_id));
        setSavedBooks(savedBookIds);
      }
    } catch (error) {
      console.error('Error fetching saved books:', error);
    }
  };

  const saveBook = async (bookId) => {
    if (!userData?.email) {
      setMessage('No user email available');
      return;
    }
    
    try {
      const response = await fetch(`${API_BASE_URL}/user/save-book?user_email=${userData.email}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ book_id: bookId })
      });

      if (response.ok) {
        setMessage('Book saved successfully!');
        setSavedBooks(prev => new Set([...prev, bookId]));
        setTimeout(() => setMessage(''), 3000);
      } else {
        const errorData = await response.json();
        setMessage(errorData.detail || 'Failed to save book');
        setTimeout(() => setMessage(''), 3000);
      }
    } catch (error) {
      console.error('Error saving book:', error);
      setMessage('Error saving book');
      setTimeout(() => setMessage(''), 3000);
    }
  };

  const unsaveBook = async (bookId) => {
    if (!userData?.email) {
      setMessage('No user email available');
      return;
    }
    
    try {
      // Find the saved book ID
      const response = await fetch(`${API_BASE_URL}/user/saved-books?user_email=${userData.email}`);
      if (response.ok) {
        const savedData = await response.json();
        const savedBook = savedData.find(saved => saved.book_id === bookId);
        
        if (savedBook) {
          const deleteResponse = await fetch(`${API_BASE_URL}/user/saved-book/${savedBook.id}?user_email=${userData.email}`, {
            method: 'DELETE'
          });

          if (deleteResponse.ok) {
            setMessage('Book removed from saved list');
            setSavedBooks(prev => {
              const newSet = new Set(prev);
              newSet.delete(bookId);
              return newSet;
            });
            setTimeout(() => setMessage(''), 3000);
          } else {
            setMessage('Failed to remove book');
            setTimeout(() => setMessage(''), 3000);
          }
        }
      }
    } catch (error) {
      console.error('Error removing saved book:', error);
      setMessage('Error removing book');
      setTimeout(() => setMessage(''), 3000);
    }
  };

  useEffect(() => {
    fetchBooks();
    if (userData?.email) {
      fetchSavedBooks();
    }
  }, [userData?.email]);

  return (
    <div className="container mt-4">
      {message && (
        <div className={`alert ${message.includes('saved') || message.includes('removed') ? 'alert-success' : 'alert-danger'} alert-dismissible fade show`}>
          {message}
          <button type="button" className="btn-close" onClick={() => setMessage('')}></button>
        </div>
      )}

      <div className="row">
        <div className="col-12">
          <div className="card mb-4">
            <div className="card-body text-center">
              <h2 className="card-title text-success">Welcome!</h2>
              <p className="card-text">Welcome to the Library System</p>
              <p className="card-text"><strong>User:</strong> {userData?.user}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card-header">
              <h3 className="mb-0">Library Books</h3>
            </div>
            <div className="card-body">
              {loadingBooks ? (
                <div className="text-center">
                  <div className="spinner-border" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </div>
                  <p className="mt-2">Loading books...</p>
                </div>
              ) : books.length > 0 ? (
                <div className="row">
                  {books.map((book) => (
                    <div key={book.id} className="col-md-6 col-lg-4 mb-3">
                      <div className="card h-100">
                        <div className="card-body">
                          <h5 className="card-title">{book.title}</h5>
                          <p className="card-text">{book.description}</p>
                          <div className="mt-3">
                            <p className="mb-1"><strong>Author:</strong> {book.author}</p>
                            <p className="mb-1"><strong>Published:</strong> {book.published_date}</p>
                          </div>
                        </div>
                        <div className="card-footer">
                          {savedBooks.has(book.id) ? (
                            <button 
                              className="btn btn-outline-danger btn-sm"
                              onClick={() => unsaveBook(book.id)}
                            >
                              ❌ Unsave
                            </button>
                          ) : (
                            <button 
                              className="btn btn-outline-primary btn-sm"
                              onClick={() => saveBook(book.id)}
                            >
                              💾 Save
                            </button>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center">
                  <p className="text-muted">No books available in the library.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home; 