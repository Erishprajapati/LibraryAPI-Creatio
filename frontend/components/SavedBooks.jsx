import React, { useState, useEffect } from 'react';

const SavedBooks = ({ userData }) => {
  const [savedBooks, setSavedBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (userData?.email) {
      fetchSavedBooks();
    } else {
      setLoading(false);
      setMessage('No user email available');
    }
  }, [userData?.email]);

  const fetchSavedBooks = async () => {
    if (!userData?.email) {
      setMessage('No user email available');
      setLoading(false);
      return;
    }
    
    try {
      const response = await fetch(`http://localhost:8000/user/saved-books?user_email=${userData.email}`);
      
      if (response.ok) {
        const data = await response.json();
        setSavedBooks(data);
      } else {
        setMessage('Failed to load saved books');
      }
    } catch (error) {
      console.error('Error fetching saved books:', error);
      setMessage('Error loading saved books');
    } finally {
      setLoading(false);
    }
  };

  const removeSavedBook = async (savedBookId) => {
    try {
      const response = await fetch(`http://localhost:8000/user/saved-book/${savedBookId}?user_email=${userData.email}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        setMessage('Book removed from saved list');
        // Refresh the saved books list
        fetchSavedBooks();
        // Clear message after 3 seconds
        setTimeout(() => setMessage(''), 3000);
      } else {
        setMessage('Failed to remove book');
      }
    } catch (error) {
      console.error('Error removing saved book:', error);
      setMessage('Error removing book');
    }
  };

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="text-center">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <h2 className="mb-4">📚 Saved Books</h2>
      
      {message && (
        <div className={`alert ${message.includes('removed') ? 'alert-success' : 'alert-danger'} alert-dismissible fade show`}>
          {message}
          <button type="button" className="btn-close" onClick={() => setMessage('')}></button>
        </div>
      )}

      {savedBooks.length === 0 ? (
        <div className="text-center mt-5">
          <h4>No saved books yet</h4>
          <p className="text-muted">Save some books from the home page to see them here!</p>
        </div>
      ) : (
        <div className="row">
          {savedBooks.map((savedBook) => (
            <div key={savedBook.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100">
                <div className="card-body">
                  <h5 className="card-title">{savedBook.book.title}</h5>
                  <h6 className="card-subtitle mb-2 text-muted">by {savedBook.book.author}</h6>
                  <p className="card-text">{savedBook.book.description}</p>
                  <p className="card-text">
                    <small className="text-muted">Published: {savedBook.book.published_date}</small>
                  </p>
                </div>
                <div className="card-footer">
                  <button 
                    className="btn btn-danger btn-sm"
                    onClick={() => removeSavedBook(savedBook.id)}
                  >
                    🗑️ Remove
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SavedBooks; 