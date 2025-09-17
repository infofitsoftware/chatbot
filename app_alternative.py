"""
Alternative Flask app using direct HTTP requests to Gemini API.
This version might help with quota issues and provides more control.
"""

from flask import Flask, render_template, request, jsonify
import os
from config import config
from models import db
from gemini_client import GeminiClient
from datetime import datetime

def create_app():
    """Application factory pattern with direct API client"""
    app = Flask(__name__)
    
    # Load configuration
    config_name = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Initialize Gemini AI client
    if app.config['GEMINI_API_KEY']:
        app.gemini_client = GeminiClient(app.config['GEMINI_API_KEY'])
        print("✅ Gemini API client initialized")
    else:
        print("Warning: GEMINI_API_KEY not found. AI features will not work.")
        app.gemini_client = None
    
    # Initialize database
    def initialize_database():
        """Initialize database connection and create tables"""
        if db.connect():
            db.create_tables()
        else:
            print("Warning: Could not connect to database. Chat history will not be saved.")
    
    # Initialize database on app creation
    initialize_database()
    
    @app.route('/')
    def index():
        """Main chat page"""
        return render_template('index.html')
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        """Handle chat messages and return AI response"""
        try:
            data = request.get_json()
            user_message = data.get('message', '').strip()
            
            if not user_message:
                return jsonify({'error': 'Message cannot be empty'}), 400
            
            # Get AI response using direct API client
            if app.gemini_client:
                try:
                    # Create a prompt for the AI
                    prompt = f"""You are a helpful AI assistant. Please respond to the following message in a friendly and informative way:

User: {user_message}

Please keep your response concise and helpful."""
                    
                    ai_response = app.gemini_client.generate_content(prompt)
                except Exception as e:
                    print(f"Error generating AI response: {e}")
                    ai_response = "I'm sorry, I'm having trouble processing your request right now. Please try again later."
            else:
                ai_response = "AI service is not available. Please check the API key configuration."
            
            # Save to database
            if db.connection:
                try:
                    db.save_message(user_message, ai_response)
                except Exception as e:
                    print(f"Error saving message to database: {e}")
            
            return jsonify({
                'user_message': user_message,
                'ai_response': ai_response,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            print(f"Error in chat endpoint: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/history', methods=['GET'])
    def get_chat_history():
        """Get recent chat history"""
        try:
            limit = request.args.get('limit', 10, type=int)
            messages = db.get_recent_messages(limit) if db.connection else []
            
            # Convert to list of dictionaries
            history = []
            for msg in messages:
                history.append({
                    'id': msg['id'],
                    'user_message': msg['user_message'],
                    'ai_response': msg['ai_response'],
                    'timestamp': msg['timestamp'].isoformat()
                })
            
            return jsonify({'messages': history})
            
        except Exception as e:
            print(f"Error getting chat history: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database_connected': db.connection is not None,
            'ai_available': app.gemini_client is not None
        }
        return jsonify(status)
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config['DEBUG']
    )
