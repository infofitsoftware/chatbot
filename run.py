#!/usr/bin/env python3
"""
Simple script to run the chat application.
This script provides an easy way to start the application with proper configuration.
"""

import os
import sys
from app import create_app

def main():
    """Main function to run the application."""
    print("🤖 Starting AI Chat Application...")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found!")
        print("   Please copy env.example to .env and configure your settings.")
        print("   cp env.example .env")
        print()
    
    # Create and run the application
    app = create_app()
    
    # Get configuration
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    debug = app.config.get('DEBUG', False)
    
    print(f"🌐 Application will be available at: http://{host}:{port}")
    print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
    print(f"🗄️  Database: {'Connected' if app.config.get('DATABASE_URL') else 'Not configured'}")
    print(f"🤖 AI Service: {'Available' if app.config.get('GEMINI_API_KEY') else 'Not configured'}")
    print("=" * 50)
    print("Press Ctrl+C to stop the application")
    print()
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
