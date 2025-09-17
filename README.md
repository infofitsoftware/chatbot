# AI Chat Application

A simple yet comprehensive chat application built with Flask, Google Gemini AI, and PostgreSQL. This project demonstrates modern web development practices including API integration, database management, testing, and deployment.

## 🚀 Features

- **AI-Powered Chat**: Integration with Google Gemini API for intelligent responses
- **Real-time Interface**: Modern, responsive chat interface with Bootstrap
- **Database Storage**: PostgreSQL integration for chat history
- **RESTful API**: Clean API endpoints for chat functionality
- **Testing Suite**: Comprehensive testing with pytest
- **CI/CD Pipeline**: Automated deployment with GitHub Actions
- **Production Ready**: Nginx, Gunicorn, and systemd service configuration

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## 🏃‍♂️ Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Google Gemini API key
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/chatbot-app.git
cd chatbot-app
```

### 2. Set Up Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy environment template
cp env.example .env

# Edit .env with your actual values
nano .env
```

### 4. Set Up Database

```bash
# Create PostgreSQL database
createdb chatbot_db

# Run database setup
psql -d chatbot_db -f database_setup.sql
```

### 5. Run the Application

```bash
python app.py
```

Visit `http://localhost:5000` to see your chat application!

## 📁 Project Structure

```
chatbot-app/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models and operations
├── requirements.txt      # Python dependencies
├── database_setup.sql    # Database schema
├── env.example          # Environment variables template
├── .env                 # Environment variables (not in git)
├── .gitignore          # Git ignore file
├── .github/
│   └── workflows/
│       └── deploy.yml   # GitHub Actions CI/CD
├── static/             # Static files
│   ├── css/
│   │   └── style.css   # Custom styles
│   ├── js/
│   │   └── chat.js     # Frontend JavaScript
│   └── images/         # Images
├── templates/          # HTML templates
│   └── index.html      # Main chat interface
├── tests/              # Test files
│   ├── __init__.py
│   └── test_app.py     # Application tests
├── STUDENT_GUIDE.md    # Comprehensive student guide
├── TESTING_GUIDE.md    # Testing instructions
├── DEPLOYMENT_GUIDE.md # Deployment guide
└── README.md          # This file
```

## 🔧 Installation

### Detailed Installation Steps

1. **Python Environment Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   # Upgrade pip
   pip install --upgrade pip
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **PostgreSQL Setup**
   ```bash
   # Install PostgreSQL (Ubuntu/Debian)
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   
   # Start PostgreSQL service
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   
   # Create database and user
   sudo -u postgres psql
   CREATE DATABASE chatbot_db;
   CREATE USER chatbot_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE chatbot_db TO chatbot_user;
   \q
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/chatbot_db

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your_secret_key_here

# Production Settings (optional)
PORT=5000
HOST=0.0.0.0
```

### Getting Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

## 💻 Usage

### Running the Application

```bash
# Development mode
python app.py

# Production mode with Gunicorn
gunicorn --bind 0.0.0.0:5000 app:app
```

### Using the Chat Interface

1. Open your browser and navigate to `http://localhost:5000`
2. Type your message in the input field
3. Press Enter or click the send button
4. View the AI response
5. Use the sidebar to check system status and load chat history

### API Usage

```bash
# Health check
curl http://localhost:5000/api/health

# Send a chat message
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'

# Get chat history
curl http://localhost:5000/api/history?limit=10
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_app.py

# Run with verbose output
pytest -v
```

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint testing
- **Database Tests**: Database operation testing
- **Frontend Tests**: User interface testing

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed testing instructions.

## 🚀 Deployment

### Local Testing

1. Follow the installation steps
2. Run the application locally
3. Test all functionality
4. Run the test suite

### AWS EC2 Deployment

1. Set up EC2 instance with Ubuntu 20.04
2. Configure security groups
3. Install dependencies (Python, PostgreSQL, Nginx)
4. Deploy application
5. Configure Nginx reverse proxy
6. Set up SSL certificate
7. Configure systemd service

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

### GitHub Actions CI/CD

The project includes automated CI/CD with GitHub Actions:

1. **Continuous Integration**: Runs tests on every push/PR
2. **Continuous Deployment**: Deploys to EC2 on main branch push
3. **Health Checks**: Verifies deployment success

### Required GitHub Secrets

Set up the following secrets in your GitHub repository:

- `GEMINI_API_KEY`: Your Google Gemini API key
- `EC2_HOST`: Your EC2 instance IP address
- `EC2_USER`: Your EC2 username (usually 'ubuntu')
- `EC2_SSH_KEY`: Your private SSH key
- `DATABASE_URL`: Your production database URL
- `SECRET_KEY`: Your Flask secret key

## 📚 API Documentation

### Endpoints

#### `GET /`
- **Description**: Main chat interface
- **Response**: HTML page

#### `GET /api/health`
- **Description**: Health check endpoint
- **Response**:
  ```json
  {
    "status": "healthy",
    "timestamp": "2024-01-01T12:00:00",
    "database_connected": true,
    "ai_available": true
  }
  ```

#### `POST /api/chat`
- **Description**: Send a chat message
- **Request Body**:
  ```json
  {
    "message": "Hello, how are you?"
  }
  ```
- **Response**:
  ```json
  {
    "user_message": "Hello, how are you?",
    "ai_response": "Hello! I'm doing well, thank you for asking.",
    "timestamp": "2024-01-01T12:00:00"
  }
  ```

#### `GET /api/history`
- **Description**: Get chat history
- **Query Parameters**:
  - `limit` (optional): Number of messages to return (default: 10)
- **Response**:
  ```json
  {
    "messages": [
      {
        "id": 1,
        "user_message": "Hello",
        "ai_response": "Hi there!",
        "timestamp": "2024-01-01T12:00:00"
      }
    ]
  }
  ```

## 🎓 Educational Value

This project demonstrates:

1. **Backend Development**: Flask web framework, RESTful APIs
2. **AI Integration**: Google Gemini API integration
3. **Database Management**: PostgreSQL with Python
4. **Frontend Development**: HTML, CSS, JavaScript, Bootstrap
5. **Testing**: Unit testing, integration testing
6. **DevOps**: CI/CD, deployment automation
7. **Version Control**: Git and GitHub best practices
8. **Cloud Deployment**: AWS EC2 deployment

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check PostgreSQL is running
   - Verify DATABASE_URL in .env
   - Ensure database exists

2. **API Key Error**
   - Verify GEMINI_API_KEY is correct
   - Check API key permissions
   - Ensure API quota is not exceeded

3. **Port Already in Use**
   - Find process using port: `lsof -i :5000`
   - Kill process or use different port

4. **Static Files Not Loading**
   - Check file paths
   - Verify Flask static file configuration
   - Clear browser cache

### Getting Help

- Check application logs
- Review error messages in browser console
- Verify environment variables
- Test API endpoints manually

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- Flask community for the excellent web framework
- Bootstrap for the responsive UI components
- PostgreSQL for reliable database functionality

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in the guides
- Review the troubleshooting section

---

**Happy Coding! 🚀**

This project is designed to be educational and demonstrate modern web development practices. Feel free to modify, extend, and learn from the code!
