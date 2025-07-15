#!/usr/bin/env python3
"""
Direct LLM test to verify API connections
"""

import os
from dotenv import load_dotenv
from crewai.llm import LLM
import requests
import json

# Load environment variables
load_dotenv()

def test_groq_llm():
    """Test Groq LLM directly"""
    print("🧪 Testing Groq LLM...")
    
    groq_key = os.getenv("groq_api_key")
    if not groq_key:
        print("❌ Groq API key not found")
        return False
    
    try:
        # Try the groq/ prefix approach first
        llm = LLM(
            model="groq/llama3-70b-8192",
            api_key=groq_key
        )
        
        # Test simple call
        response = llm.call([{"role": "user", "content": "Say hello from Karl Franz, Emperor of the Empire!"}])
        # Handle both string and object responses
        if hasattr(response, 'content'):
            content = response.content
        else:
            content = str(response)
        print(f"✅ Groq response: {content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Groq LLM failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        print(f"   Full traceback:")
        traceback.print_exc()
        return False

def test_cerebras_llm():
    """Test Cerebras LLM directly"""
    print("\n🧪 Testing Cerebras LLM...")
    
    cerebras_key = os.getenv("Cerebras_api")
    if not cerebras_key:
        print("❌ Cerebras API key not found")
        return False
    
    try:
        # Try different approaches for Cerebras
        # First try: use openai/ prefix with custom base_url
        llm = LLM(
            model="openai/llama3.1-8b",
            api_key=cerebras_key,
            base_url="https://api.cerebras.ai/v1"
        )
        
        # Test simple call
        response = llm.call([{"role": "user", "content": "Say hello from a Witch Hunter!"}])
        # Handle both string and object responses
        if hasattr(response, 'content'):
            content = response.content
        else:
            content = str(response)
        print(f"✅ Cerebras response: {content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Cerebras LLM failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        print(f"   Full traceback:")
        traceback.print_exc()
        return False

def test_groq_direct():
    """Test Groq API directly with requests"""
    print("\n🧪 Testing Groq API directly with requests...")

    groq_key = os.getenv("groq_api_key")
    if not groq_key:
        print("❌ Groq API key not found")
        return False

    try:
        headers = {
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "user", "content": "Say hello from Karl Franz, Emperor of the Empire!"}
            ],
            "max_tokens": 100
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            print(f"✅ Groq direct response: {content[:100]}...")
            return True
        else:
            print(f"❌ Groq direct failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Groq direct failed: {e}")
        return False

def test_cerebras_direct():
    """Test Cerebras API directly with requests"""
    print("\n🧪 Testing Cerebras API directly with requests...")

    cerebras_key = os.getenv("Cerebras_api")
    if not cerebras_key:
        print("❌ Cerebras API key not found")
        return False

    try:
        headers = {
            "Authorization": f"Bearer {cerebras_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3.1-8b",
            "messages": [
                {"role": "user", "content": "Say hello from a Witch Hunter!"}
            ],
            "max_tokens": 100
        }

        response = requests.post(
            "https://api.cerebras.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            print(f"✅ Cerebras direct response: {content[:100]}...")
            return True
        else:
            print(f"❌ Cerebras direct failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Cerebras direct failed: {e}")
        return False

def main():
    """Main test function"""
    print("🔑 API Key Direct LLM Test")
    print("=" * 40)

    # Test CrewAI LLM wrapper
    groq_success = test_groq_llm()
    cerebras_success = test_cerebras_llm()

    # Test direct API calls
    groq_direct_success = test_groq_direct()
    cerebras_direct_success = test_cerebras_direct()

    print("\n" + "=" * 40)
    print("📊 RESULTS:")
    print(f"  Groq LLM (CrewAI): {'✅' if groq_success else '❌'}")
    print(f"  Cerebras LLM (CrewAI): {'✅' if cerebras_success else '❌'}")
    print(f"  Groq API (Direct): {'✅' if groq_direct_success else '❌'}")
    print(f"  Cerebras API (Direct): {'✅' if cerebras_direct_success else '❌'}")

    if groq_direct_success and cerebras_direct_success:
        print("\n🎉 Both APIs working directly! Issue is with CrewAI LLM wrapper.")
    elif groq_success and cerebras_success:
        print("\n🎉 Both LLMs working! API keys are correctly configured.")
    else:
        print("\n⚠️ Some APIs failed. Check API keys and network connection.")

if __name__ == "__main__":
    main()
