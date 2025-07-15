#!/usr/bin/env python3
"""
Simple API test using OpenAI client format
"""

import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

def test_groq_api():
    """Test Groq API with simple HTTP request"""
    print("🧪 Testing Groq API...")
    
    groq_key = os.getenv("groq_api_key")
    if not groq_key:
        print("❌ Groq API key not found")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "user", "content": "Say hello from Karl Franz!"}
            ],
            "max_tokens": 50
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            message = result["choices"][0]["message"]["content"]
            print(f"✅ Groq response: {message[:100]}...")
            return True
        else:
            print(f"❌ Groq API error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Groq API failed: {e}")
        return False

def test_cerebras_api():
    """Test Cerebras API with simple HTTP request"""
    print("\n🧪 Testing Cerebras API...")
    
    cerebras_key = os.getenv("Cerebras_api")
    if not cerebras_key:
        print("❌ Cerebras API key not found")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {cerebras_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama3.1-8b",
            "messages": [
                {"role": "user", "content": "Say hello from a Witch Hunter!"}
            ],
            "max_tokens": 50
        }
        
        response = requests.post(
            "https://api.cerebras.ai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            message = result["choices"][0]["message"]["content"]
            print(f"✅ Cerebras response: {message[:100]}...")
            return True
        else:
            print(f"❌ Cerebras API error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Cerebras API failed: {e}")
        return False

def main():
    """Main test function"""
    print("🔑 Simple API Connection Test")
    print("=" * 40)
    
    # Show API keys (masked)
    groq_key = os.getenv("groq_api_key", "NOT FOUND")
    cerebras_key = os.getenv("Cerebras_api", "NOT FOUND")
    
    print(f"Groq Key: {groq_key[:10]}...{groq_key[-5:] if len(groq_key) > 15 else groq_key}")
    print(f"Cerebras Key: {cerebras_key[:10]}...{cerebras_key[-5:] if len(cerebras_key) > 15 else cerebras_key}")
    print()
    
    # Test both APIs
    groq_success = test_groq_api()
    cerebras_success = test_cerebras_api()
    
    print("\n" + "=" * 40)
    print("📊 RESULTS:")
    print(f"  Groq API: {'✅' if groq_success else '❌'}")
    print(f"  Cerebras API: {'✅' if cerebras_success else '❌'}")
    
    if groq_success or cerebras_success:
        print("\n🎉 At least one API is working! We can proceed with CrewAI.")
    else:
        print("\n⚠️ Both APIs failed. Check API keys and network connection.")

if __name__ == "__main__":
    main()
