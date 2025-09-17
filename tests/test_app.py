import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import our app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Set testing environment
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app()
    app.config['TESTING'] = True
    app.config['DATABASE_URL'] = os.environ.get('TEST_DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/test_chatbot_db')
    app.config['GEMINI_API_KEY'] = 'test-api-key'
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        # Initialize database for testing
        if db.connect():
            db.create_tables()
        yield app
        # Clean up after test
        if db.connection:
            db.disconnect()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

class TestHealthEndpoint:
    """Test the health check endpoint."""
    
    def test_health_check(self, client):
        """Test that health check returns 200."""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'status' in data
        assert 'timestamp' in data
        assert 'database_connected' in data
        assert 'ai_available' in data

class TestChatEndpoint:
    """Test the chat endpoint."""
    
    @patch('app.genai.GenerativeModel')
    def test_chat_success(self, mock_model, client):
        """Test successful chat request."""
        # Mock the Gemini API response
        mock_response = MagicMock()
        mock_response.text = "Hello! How can I help you today?"
        mock_model.return_value.generate_content.return_value = mock_response
        
        response = client.post('/api/chat', 
                             json={'message': 'Hello'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'user_message' in data
        assert 'ai_response' in data
        assert 'timestamp' in data
        assert data['user_message'] == 'Hello'
    
    def test_chat_empty_message(self, client):
        """Test chat with empty message."""
        response = client.post('/api/chat', 
                             json={'message': ''})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_chat_missing_message(self, client):
        """Test chat without message field."""
        response = client.post('/api/chat', 
                             json={})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

class TestHistoryEndpoint:
    """Test the chat history endpoint."""
    
    def test_history_endpoint(self, client):
        """Test getting chat history."""
        response = client.get('/api/history')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'messages' in data
        assert isinstance(data['messages'], list)
    
    def test_history_with_limit(self, client):
        """Test getting chat history with limit."""
        response = client.get('/api/history?limit=5')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'messages' in data

class TestMainPage:
    """Test the main page."""
    
    def test_index_page(self, client):
        """Test that the index page loads."""
        response = client.get('/')
        
        assert response.status_code == 200
        assert b'AI Chat Application' in response.data

class TestDatabase:
    """Test database operations."""
    
    def test_database_connection(self, app):
        """Test database connection."""
        with app.app_context():
            assert db.connect() == True
            db.disconnect()
    
    def test_save_message(self, app):
        """Test saving a message to database."""
        with app.app_context():
            if db.connect():
                result = db.save_message("Test message", "Test response")
                assert result is not None
                assert 'id' in result
                db.disconnect()
    
    def test_get_messages(self, app):
        """Test retrieving messages from database."""
        with app.app_context():
            if db.connect():
                messages = db.get_recent_messages(5)
                assert isinstance(messages, list)
                db.disconnect()

if __name__ == '__main__':
    pytest.main([__file__])
