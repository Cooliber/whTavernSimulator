#!/usr/bin/env python3
"""
Test configuration loading
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔧 Testing Configuration Loading")
print("=" * 40)

# Test environment variables directly
print("📋 Environment Variables:")
print(f"  groq_api_key: {os.getenv('groq_api_key', 'NOT FOUND')[:20]}...")
print(f"  Cerebras_api: {os.getenv('Cerebras_api', 'NOT FOUND')[:20]}...")

# Test config import
try:
    from config import api_config
    print("\n📋 Config Object:")
    print(f"  groq_api_key: {api_config.groq_api_key[:20] if api_config.groq_api_key else 'NOT FOUND'}...")
    print(f"  cerebras_api_key: {api_config.cerebras_api_key[:20] if api_config.cerebras_api_key else 'NOT FOUND'}...")
    print(f"  groq_base_url: {api_config.groq_base_url}")
    print(f"  cerebras_base_url: {api_config.cerebras_base_url}")
except Exception as e:
    print(f"❌ Config import failed: {e}")
