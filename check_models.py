#!/usr/bin/env python3
"""
Script to check available Gemini models and their supported methods.
Run this script to see which models are available with your API key.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

def check_available_models():
    """Check and display available Gemini models."""
    # Load environment variables
    load_dotenv()
    
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables.")
        print("   Please make sure your .env file contains the API key.")
        return
    
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        print("🔍 Checking available Gemini models...")
        print("=" * 60)
        
        # List all models
        models = list(genai.list_models())
        
        if not models:
            print("❌ No models found. Check your API key and internet connection.")
            return
        
        print(f"✅ Found {len(models)} available models:")
        print()
        
        # Group models by type
        generate_content_models = []
        other_models = []
        
        for model in models:
            if "generateContent" in model.supported_generation_methods:
                generate_content_models.append(model)
            else:
                other_models.append(model)
        
        # Display models that support generateContent
        if generate_content_models:
            print("🤖 Models that support generateContent (recommended for chat):")
            print("-" * 50)
            for model in generate_content_models:
                print(f"  • {model.name}")
                if hasattr(model, 'display_name'):
                    print(f"    Display Name: {model.display_name}")
                print(f"    Supported Methods: {', '.join(model.supported_generation_methods)}")
                print()
        
        # Display other models
        if other_models:
            print("🔧 Other available models:")
            print("-" * 30)
            for model in other_models:
                print(f"  • {model.name}")
                if hasattr(model, 'display_name'):
                    print(f"    Display Name: {model.display_name}")
                print(f"    Supported Methods: {', '.join(model.supported_generation_methods)}")
                print()
        
        # Recommend a model
        if generate_content_models:
            recommended = None
            for model in generate_content_models:
                if 'flash' in model.name.lower():
                    recommended = model.name
                    break
                elif 'pro' in model.name.lower():
                    recommended = model.name
                    break
            
            if recommended:
                print("💡 Recommended model for chat application:")
                print(f"   {recommended}")
                print()
                print("To use this model, update your app.py file:")
                print(f"   app.gemini_model = genai.GenerativeModel('{recommended}')")
        
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        print()
        print("Possible issues:")
        print("1. Invalid API key")
        print("2. No internet connection")
        print("3. API quota exceeded")
        print("4. API service temporarily unavailable")

def test_model(model_name):
    """Test a specific model with a simple request."""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found.")
        return
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        print(f"🧪 Testing model: {model_name}")
        response = model.generate_content("Hello, how are you?")
        
        print("✅ Model test successful!")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")

if __name__ == "__main__":
    print("Google Gemini API Model Checker")
    print("=" * 40)
    print()
    
    check_available_models()
    
    # Test the recommended model
    print("\n" + "=" * 60)
    print("Testing the updated model...")
    test_model('gemini-1.5-flash')
