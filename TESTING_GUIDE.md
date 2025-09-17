# Testing Guide for Chat Application

## Table of Contents
1. [Local Testing Setup](#local-testing-setup)
2. [Environment Configuration](#environment-configuration)
3. [Database Testing](#database-testing)
4. [API Testing](#api-testing)
5. [Frontend Testing](#frontend-testing)
6. [Integration Testing](#integration-testing)
7. [Troubleshooting](#troubleshooting)

## Local Testing Setup

### Prerequisites
Before testing, ensure you have:
- Python 3.8+ installed
- PostgreSQL installed and running
- Google Gemini API key
- All dependencies installed (`pip install -r requirements.txt`)

### Step 1: Environment Setup

1. **Copy environment template:**
   ```bash
   cp env.example .env
   ```

2. **Edit .env file with your actual values:**
   ```bash
   # Get your Gemini API key from: https://makersuite.google.com/app/apikey
   GEMINI_API_KEY=your_actual_api_key_here
   
   # Set up your local database
   DATABASE_URL=postgresql://username:password@localhost:5432/chatbot_db
   
   # Flask settings
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   ```

### Step 2: Database Setup

1. **Create PostgreSQL database:**
   ```bash
   # Connect to PostgreSQL
   psql -U postgres
   
   # Create database
   CREATE DATABASE chatbot_db;
   
   # Create user (optional)
   CREATE USER chatbot_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE chatbot_db TO chatbot_user;
   
   # Exit psql
   \q
   ```

2. **Run database setup script:**
   ```bash
   psql -U postgres -d chatbot_db -f database_setup.sql
   ```

3. **Verify database setup:**
   ```bash
   psql -U postgres -d chatbot_db -c "SELECT * FROM messages LIMIT 3;"
   ```

## Environment Configuration

### Testing Different Environments

1. **Development Environment:**
   ```bash
   export FLASK_ENV=development
   python app.py
   ```

2. **Production-like Environment:**
   ```bash
   export FLASK_ENV=production
   export PORT=5000
   python app.py
   ```

## Database Testing

### Test Database Connection

Create a test script `test_db.py`:
```python
import os
from dotenv import load_dotenv
from models import db

load_dotenv()

def test_database_connection():
    """Test database connection and operations"""
    print("Testing database connection...")
    
    if db.connect():
        print("✅ Database connection successful")
        
        # Test table creation
        if db.create_tables():
            print("✅ Tables created successfully")
        
        # Test message insertion
        result = db.save_message("Test message", "Test response")
        if result:
            print(f"✅ Message saved with ID: {result['id']}")
        
        # Test message retrieval
        messages = db.get_recent_messages(5)
        print(f"✅ Retrieved {len(messages)} messages")
        
        # Test message count
        count = db.get_message_count()
        print(f"✅ Total messages: {count}")
        
        db.disconnect()
        print("✅ Database connection closed")
        return True
    else:
        print("❌ Database connection failed")
        return False

if __name__ == "__main__":
    test_database_connection()
```

Run the test:
```bash
python test_db.py
```

## API Testing

### Manual API Testing with curl

1. **Health Check:**
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **Send Chat Message:**
   ```bash
   curl -X POST http://localhost:5000/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello, how are you?"}'
   ```

3. **Get Chat History:**
   ```bash
   curl http://localhost:5000/api/history?limit=5
   ```

### API Testing with Python

Create `test_api.py`:
```python
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health_endpoint():
    """Test health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Database: {'Connected' if data['database_connected'] else 'Disconnected'}")
            print(f"   AI: {'Available' if data['ai_available'] else 'Unavailable'}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_chat_endpoint():
    """Test chat endpoint"""
    try:
        payload = {"message": "Hello, this is a test message"}
        response = requests.post(
            f"{BASE_URL}/api/chat",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat endpoint working")
            print(f"   User message: {data['user_message']}")
            print(f"   AI response: {data['ai_response'][:50]}...")
            return True
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")
        return False

def test_history_endpoint():
    """Test history endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/history?limit=3")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ History endpoint working - {len(data['messages'])} messages")
            return True
        else:
            print(f"❌ History endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ History endpoint error: {e}")
        return False

if __name__ == "__main__":
    print("Testing API endpoints...")
    print("=" * 40)
    
    health_ok = test_health_endpoint()
    chat_ok = test_chat_endpoint()
    history_ok = test_history_endpoint()
    
    print("=" * 40)
    if all([health_ok, chat_ok, history_ok]):
        print("🎉 All API tests passed!")
    else:
        print("❌ Some API tests failed")
```

Run the API test:
```bash
python test_api.py
```

## Frontend Testing

### Manual Frontend Testing

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Open browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Test the following features:**
   - [ ] Page loads without errors
   - [ ] Sidebar shows connection status
   - [ ] Can type in message input
   - [ ] Send button works
   - [ ] Enter key sends message
   - [ ] AI responses appear
   - [ ] Chat history loads
   - [ ] Clear chat works
   - [ ] Responsive design works on mobile

### Browser Developer Tools Testing

1. **Open Developer Tools (F12)**
2. **Check Console for errors**
3. **Test Network tab:**
   - Verify API calls are made
   - Check response times
   - Ensure no failed requests

4. **Test Responsive Design:**
   - Use device emulation
   - Test different screen sizes
   - Verify mobile layout

## Integration Testing

### End-to-End Testing Script

Create `test_integration.py`:
```python
import requests
import time
import json

BASE_URL = "http://localhost:5000"

def test_complete_chat_flow():
    """Test complete chat flow from frontend to database"""
    print("Testing complete chat flow...")
    
    # Test 1: Health check
    health_response = requests.get(f"{BASE_URL}/api/health")
    assert health_response.status_code == 200, "Health check failed"
    print("✅ Health check passed")
    
    # Test 2: Send multiple messages
    test_messages = [
        "Hello, how are you?",
        "What is Python?",
        "Tell me a joke"
    ]
    
    for i, message in enumerate(test_messages):
        print(f"Testing message {i+1}: {message}")
        
        response = requests.post(
            f"{BASE_URL}/api/chat",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"message": message})
        )
        
        assert response.status_code == 200, f"Chat request {i+1} failed"
        data = response.json()
        assert "ai_response" in data, "No AI response received"
        print(f"✅ Message {i+1} processed successfully")
        
        # Small delay between messages
        time.sleep(1)
    
    # Test 3: Verify messages in database
    history_response = requests.get(f"{BASE_URL}/api/history?limit=10")
    assert history_response.status_code == 200, "History request failed"
    
    history_data = history_response.json()
    assert len(history_data["messages"]) >= len(test_messages), "Not all messages saved"
    print(f"✅ All {len(test_messages)} messages saved to database")
    
    print("🎉 Complete chat flow test passed!")

if __name__ == "__main__":
    try:
        test_complete_chat_flow()
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
```

Run integration test:
```bash
python test_integration.py
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Issues
**Problem:** "psycopg2.OperationalError: could not connect to server"

**Solutions:**
- Check if PostgreSQL is running: `sudo systemctl status postgresql`
- Verify database URL in .env file
- Check if database exists: `psql -l`
- Verify user permissions

#### 2. Gemini API Issues
**Problem:** "Invalid API key" or "API quota exceeded"

**Solutions:**
- Verify API key is correct in .env file
- Check API key permissions in Google AI Studio
- Verify API quota limits
- Test API key with curl:
  ```bash
  curl -H "Content-Type: application/json" \
       -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
       "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_API_KEY"
  ```

#### 3. Flask Application Issues
**Problem:** "ModuleNotFoundError" or import errors

**Solutions:**
- Ensure virtual environment is activated
- Install all dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version`
- Verify file structure

#### 4. Frontend Issues
**Problem:** Static files not loading or JavaScript errors

**Solutions:**
- Check browser console for errors
- Verify static file paths
- Clear browser cache
- Check if Flask is serving static files correctly

#### 5. Port Issues
**Problem:** "Address already in use"

**Solutions:**
- Find process using port: `lsof -i :5000` (macOS/Linux) or `netstat -ano | findstr :5000` (Windows)
- Kill the process or use different port
- Set PORT environment variable: `export PORT=5001`

### Testing Checklist

Before deploying, ensure:
- [ ] All unit tests pass
- [ ] API endpoints respond correctly
- [ ] Database operations work
- [ ] Frontend loads without errors
- [ ] Chat functionality works end-to-end
- [ ] Error handling works properly
- [ ] Application handles edge cases
- [ ] Performance is acceptable
- [ ] Security considerations are addressed

### Performance Testing

Test with multiple concurrent requests:
```python
import concurrent.futures
import requests
import time

def send_chat_request(message_id):
    response = requests.post(
        "http://localhost:5000/api/chat",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"message": f"Test message {message_id}"})
    )
    return response.status_code == 200

# Test with 10 concurrent requests
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(send_chat_request, i) for i in range(10)]
    results = [future.result() for future in concurrent.futures.as_completed(futures)]

print(f"Successful requests: {sum(results)}/10")
```

This comprehensive testing guide ensures your chat application works correctly before deployment.
