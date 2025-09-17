# Student Guide: Building a Chat Application with LLM API

## Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Step 1: Setting Up the Development Environment](#step-1-setting-up-the-development-environment)
4. [Step 2: Creating the Flask Backend](#step-2-creating-the-flask-backend)
5. [Step 3: Integrating Google Gemini API](#step-3-integrating-google-gemini-api)
6. [Step 4: Creating the Frontend](#step-4-creating-the-frontend)
7. [Step 5: Setting Up PostgreSQL Database](#step-5-setting-up-postgresql-database)
8. [Step 6: Testing Locally](#step-6-testing-locally)
9. [Step 7: Setting Up GitHub Repository](#step-7-setting-up-github-repository)
10. [Step 8: Deploying to AWS EC2](#step-8-deploying-to-aws-ec2)
11. [Step 9: Setting Up CI/CD with GitHub Actions](#step-9-setting-up-cicd-with-github-actions)
12. [Troubleshooting](#troubleshooting)

## Project Overview

In this project, you will learn how to:
- Build a web application using Flask (Python backend)
- Integrate with Google Gemini LLM API
- Create a responsive frontend with HTML, CSS, Bootstrap, and JavaScript
- Use PostgreSQL database to store chat history
- Test your application locally
- Deploy to AWS EC2 using GitHub Actions CI/CD

### Application Features
- Simple chat interface
- Integration with Google Gemini API for AI responses
- Chat history storage in PostgreSQL
- Responsive design using Bootstrap
- Real-time chat experience

## Prerequisites

Before starting, ensure you have:
1. **Python 3.8+** installed on your computer
2. **Git** installed for version control
3. **A Google Cloud account** with Gemini API access
4. **An AWS account** for deployment
5. **A GitHub account** for code repository
6. **Basic knowledge** of Python, HTML, CSS, and JavaScript

## Step 1: Setting Up the Development Environment

### 1.1 Create Project Directory
```bash
mkdir chatbot-app
cd chatbot-app
```

### 1.2 Set Up Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 1.3 Install Required Packages
Create a `requirements.txt` file with the following dependencies:
```
Flask==2.3.3
google-generativeai==0.3.2
psycopg2-binary==2.9.7
python-dotenv==1.0.0
gunicorn==21.2.0
```

Install the packages:
```bash
pip install -r requirements.txt
```

## Step 2: Creating the Flask Backend

### 2.1 Project Structure
Create the following directory structure:
```
chatbot-app/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in git)
├── .gitignore           # Git ignore file
├── static/              # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/           # HTML templates
│   └── index.html
└── README.md           # Project documentation
```

### 2.2 Environment Variables
Create a `.env` file (this will contain sensitive information):
```
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/chatbot_db
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

**Important**: Never commit the `.env` file to version control!

## Step 3: Integrating Google Gemini API

### 3.1 Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key to your `.env` file

### 3.2 Understanding the API Integration
The Gemini API allows you to send text prompts and receive AI-generated responses. We'll use it to create intelligent chat responses.

## Step 4: Creating the Frontend

### 4.1 HTML Structure
We'll create a responsive chat interface using Bootstrap for styling and JavaScript for interactivity.

### 4.2 Key Frontend Concepts
- **Bootstrap**: For responsive design and UI components
- **JavaScript**: For handling user interactions and API calls
- **CSS**: For custom styling
- **AJAX**: For sending requests to the backend without page refresh

## Step 5: Setting Up PostgreSQL Database

### 5.1 Database Design
We'll create a simple table to store chat messages:
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5.2 Database Connection
We'll use `psycopg2` to connect to PostgreSQL and store chat history.

## Step 6: Testing Locally

### 6.1 Running the Application
```bash
# Make sure your virtual environment is activated
python app.py
```

### 6.2 Testing Checklist
- [ ] Application starts without errors
- [ ] Frontend loads correctly
- [ ] Can send messages and receive AI responses
- [ ] Chat history is saved to database
- [ ] Responsive design works on different screen sizes

## Step 7: Setting Up GitHub Repository

### 7.1 Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit: Chat application setup"
```

### 7.2 Create GitHub Repository
1. Go to GitHub.com
2. Create a new repository
3. Connect your local repository to GitHub:
```bash
git remote add origin https://github.com/yourusername/chatbot-app.git
git push -u origin main
```

## Step 8: Deploying to AWS EC2

### 8.1 Setting Up EC2 Instance
1. Launch an EC2 instance (Ubuntu 20.04 LTS)
2. Configure security groups (open ports 22, 80, 443)
3. Connect to your instance via SSH

### 8.2 Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install Nginx
sudo apt install nginx -y

# Install Git
sudo apt install git -y
```

### 8.3 Application Deployment
```bash
# Clone your repository
git clone https://github.com/yourusername/chatbot-app.git
cd chatbot-app

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
nano .env
# Add your production environment variables
```

## Step 9: Setting Up CI/CD with GitHub Actions

### 9.1 GitHub Secrets
Set up the following secrets in your GitHub repository:
- `GEMINI_API_KEY`: Your Gemini API key
- `EC2_HOST`: Your EC2 instance IP address
- `EC2_USER`: Your EC2 username (usually 'ubuntu')
- `EC2_SSH_KEY`: Your private SSH key
- `DATABASE_URL`: Your production database URL

### 9.2 GitHub Actions Workflow
We'll create a workflow that:
1. Tests the application
2. Deploys to EC2 when code is pushed to main branch
3. Restarts the application service

## Troubleshooting

### Common Issues and Solutions

#### 1. API Key Issues
- **Problem**: "Invalid API key" error
- **Solution**: Verify your Gemini API key is correct and has proper permissions

#### 2. Database Connection Issues
- **Problem**: Cannot connect to PostgreSQL
- **Solution**: Check database URL, ensure PostgreSQL is running, verify credentials

#### 3. Deployment Issues
- **Problem**: Application not starting on EC2
- **Solution**: Check logs, verify environment variables, ensure all dependencies are installed

#### 4. Frontend Not Loading
- **Problem**: Static files not loading
- **Solution**: Check Nginx configuration, verify file paths

### Getting Help
- Check application logs: `journalctl -u your-app-name`
- Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
- Verify environment variables are set correctly
- Test API endpoints manually using curl or Postman

## Learning Outcomes

After completing this project, you will understand:
1. **Backend Development**: How to create REST APIs with Flask
2. **LLM Integration**: How to integrate AI APIs into applications
3. **Frontend Development**: How to create responsive web interfaces
4. **Database Management**: How to work with PostgreSQL
5. **Version Control**: How to use Git and GitHub effectively
6. **DevOps**: How to deploy applications to cloud servers
7. **CI/CD**: How to automate deployment processes
8. **Environment Management**: How to handle sensitive configuration

## Next Steps

Once you've completed this project, consider these enhancements:
- Add user authentication
- Implement real-time chat using WebSockets
- Add file upload capabilities
- Create a mobile app version
- Add more AI features (image generation, etc.)
- Implement chat rooms or channels
- Add message search functionality

Remember: The goal is to learn the development process, not to create a perfect application. Focus on understanding each step and the reasoning behind it.
