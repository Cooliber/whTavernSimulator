"""
LLM Service for Grok and Cerebras API integration
Handles all AI model communications for tavern agents
"""

import json
import time
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config import api_config

class LLMProvider(Enum):
    GROQ = "groq"  # Changed from GROK to GROQ for clarity
    CEREBRAS = "cerebras"
    OPENAI = "openai"

@dataclass
class LLMRequest:
    """Structure for LLM API requests"""
    prompt: str
    system_message: str = ""
    max_tokens: int = 500
    temperature: float = 0.7
    provider: LLMProvider = LLMProvider.GROQ
    agent_name: str = ""
    context: Dict[str, Any] = None

@dataclass
class LLMResponse:
    """Structure for LLM API responses"""
    content: str
    provider: LLMProvider
    success: bool
    error_message: str = ""
    tokens_used: int = 0
    response_time: float = 0.0

class LLMService:
    """Service for managing LLM API calls"""
    
    def __init__(self):
        self.request_history = []
        self.provider_stats = {
            LLMProvider.GROQ: {"requests": 0, "successes": 0, "avg_response_time": 0.0},
            LLMProvider.CEREBRAS: {"requests": 0, "successes": 0, "avg_response_time": 0.0},
            LLMProvider.OPENAI: {"requests": 0, "successes": 0, "avg_response_time": 0.0}
        }
    
    def call_llm(self, request: LLMRequest) -> LLMResponse:
        """Main method to call appropriate LLM provider"""
        start_time = time.time()
        
        try:
            if request.provider == LLMProvider.GROQ:
                response = self._call_groq(request)
            elif request.provider == LLMProvider.CEREBRAS:
                response = self._call_cerebras(request)
            elif request.provider == LLMProvider.OPENAI:
                response = self._call_openai(request)
            else:
                response = self._create_mock_response(request)
            
            response.response_time = time.time() - start_time
            
            # Update statistics
            self._update_stats(request.provider, response)
            
            # Store request history
            self.request_history.append({
                "request": request,
                "response": response,
                "timestamp": time.time()
            })
            
            return response
            
        except Exception as e:
            return LLMResponse(
                content=f"Error calling {request.provider.value}: {str(e)}",
                provider=request.provider,
                success=False,
                error_message=str(e),
                response_time=time.time() - start_time
            )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((requests.RequestException, requests.Timeout))
    )
    def _call_groq(self, request: LLMRequest) -> LLMResponse:
        """Call Groq API for complex reasoning with retry mechanism"""
        if not api_config.groq_api_key:
            return self._create_mock_response(request, "No Groq API key configured")

        headers = {
            "Authorization": f"Bearer {api_config.groq_api_key}",
            "Content-Type": "application/json"
        }

        # Prepare Groq-specific prompt for Warhammer Fantasy context
        system_prompt = self._prepare_groq_system_prompt(request)
        user_prompt = self._prepare_groq_user_prompt(request)

        payload = {
            "model": "llama3-70b-8192",  # Groq model name for complex reasoning
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "stream": False
        }

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                tokens_used = data.get("usage", {}).get("total_tokens", 0)

                return LLMResponse(
                    content=content,
                    provider=LLMProvider.GROQ,
                    success=True,
                    tokens_used=tokens_used
                )
            else:
                return LLMResponse(
                    content=f"Groq API error: {response.status_code}",
                    provider=LLMProvider.GROQ,
                    success=False,
                    error_message=f"HTTP {response.status_code}: {response.text}"
                )

        except requests.RequestException as e:
            return self._create_mock_response(request, f"Groq connection error: {str(e)}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        retry=retry_if_exception_type((requests.RequestException, requests.Timeout))
    )
    def _call_cerebras(self, request: LLMRequest) -> LLMResponse:
        """Call Cerebras API for fast responses with retry mechanism"""
        if not api_config.cerebras_api_key:
            return self._create_mock_response(request, "No Cerebras API key configured")
        
        headers = {
            "Authorization": f"Bearer {api_config.cerebras_api_key}",
            "Content-Type": "application/json"
        }
        
        # Prepare Cerebras-specific prompt for quick responses
        system_prompt = self._prepare_cerebras_system_prompt(request)
        user_prompt = self._prepare_cerebras_user_prompt(request)
        
        payload = {
            "model": "llama3.1-8b",  # Cerebras model name
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": min(request.max_tokens, 300),  # Cerebras optimized for shorter responses
            "temperature": request.temperature,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{api_config.cerebras_base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=15  # Faster timeout for Cerebras
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                tokens_used = data.get("usage", {}).get("total_tokens", 0)
                
                return LLMResponse(
                    content=content,
                    provider=LLMProvider.CEREBRAS,
                    success=True,
                    tokens_used=tokens_used
                )
            else:
                return LLMResponse(
                    content=f"Cerebras API error: {response.status_code}",
                    provider=LLMProvider.CEREBRAS,
                    success=False,
                    error_message=f"HTTP {response.status_code}: {response.text}"
                )
                
        except requests.RequestException as e:
            return self._create_mock_response(request, f"Cerebras connection error: {str(e)}")
    
    def _call_openai(self, request: LLMRequest) -> LLMResponse:
        """Call OpenAI API as fallback"""
        if not api_config.openai_api_key:
            return self._create_mock_response(request, "No OpenAI API key configured")
        
        headers = {
            "Authorization": f"Bearer {api_config.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": request.system_message or "You are a helpful assistant in a Warhammer Fantasy tavern."},
                {"role": "user", "content": request.prompt}
            ],
            "max_tokens": request.max_tokens,
            "temperature": request.temperature
        }
        
        try:
            response = requests.post(
                f"{api_config.openai_base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                tokens_used = data.get("usage", {}).get("total_tokens", 0)
                
                return LLMResponse(
                    content=content,
                    provider=LLMProvider.OPENAI,
                    success=True,
                    tokens_used=tokens_used
                )
            else:
                return self._create_mock_response(request, f"OpenAI API error: {response.status_code}")
                
        except requests.RequestException as e:
            return self._create_mock_response(request, f"OpenAI connection error: {str(e)}")
    
    def _prepare_groq_system_prompt(self, request: LLMRequest) -> str:
        """Prepare system prompt optimized for Groq's reasoning capabilities"""
        base_prompt = f"""You are {request.agent_name}, a character in a Warhammer Fantasy tavern simulation.

SETTING: The Old World of Warhammer Fantasy - a dark, gritty medieval fantasy setting where Chaos threatens civilization.

YOUR ROLE: {request.system_message}

REASONING STYLE: Provide detailed, strategic thinking. Consider multiple factors, potential consequences, and long-term implications. Show your reasoning process step by step.

RESPONSE FORMAT:
1. Brief analysis of the situation
2. Your reasoning process
3. Your decision/action
4. Expected outcomes

Keep responses authentic to the Warhammer Fantasy setting with appropriate tone and vocabulary."""

        return base_prompt

    def _prepare_groq_user_prompt(self, request: LLMRequest) -> str:
        """Prepare user prompt for Groq with context"""
        context_str = ""
        if request.context:
            context_str = f"\nCURRENT CONTEXT:\n{json.dumps(request.context, indent=2)}\n"

        return f"{context_str}\nSITUATION: {request.prompt}\n\nProvide your detailed analysis and decision:"
    
    def _prepare_cerebras_system_prompt(self, request: LLMRequest) -> str:
        """Prepare system prompt optimized for Cerebras' speed"""
        return f"""You are {request.agent_name} in a Warhammer Fantasy tavern. {request.system_message}

Respond quickly and decisively. Be concise but authentic to the dark fantasy setting. Focus on immediate actions rather than long-term planning."""
    
    def _prepare_cerebras_user_prompt(self, request: LLMRequest) -> str:
        """Prepare user prompt for Cerebras - concise and action-oriented"""
        return f"SITUATION: {request.prompt}\n\nYour immediate response:"
    
    def _create_mock_response(self, request: LLMRequest, error_msg: str = "") -> LLMResponse:
        """Create mock response for testing or when APIs unavailable"""
        mock_responses = {
            "Karczmarz": "I carefully assess the tavern situation and consider the best course of action to maintain order and protect my establishment.",
            "Skrytobójca": "I remain hidden in the shadows, gathering information while staying alert for threats and opportunities.",
            "Wiedźma": "The mystical energies reveal hidden truths about this situation. I sense deeper currents at work.",
            "Zwiadowca": "I report what I've observed and prepare to gather more intelligence about the developing situation.",
            "Czempion": "Chaos stirs within me. I seek opportunities to spread discord and challenge the established order."
        }
        
        content = mock_responses.get(request.agent_name, "I observe the situation carefully and prepare to act.")
        
        if error_msg:
            content = f"[MOCK RESPONSE - {error_msg}] {content}"
        
        return LLMResponse(
            content=content,
            provider=request.provider,
            success=not bool(error_msg),
            error_message=error_msg
        )
    
    def _update_stats(self, provider: LLMProvider, response: LLMResponse):
        """Update provider statistics"""
        stats = self.provider_stats[provider]
        stats["requests"] += 1
        
        if response.success:
            stats["successes"] += 1
        
        # Update average response time
        if stats["requests"] == 1:
            stats["avg_response_time"] = response.response_time
        else:
            stats["avg_response_time"] = (
                (stats["avg_response_time"] * (stats["requests"] - 1) + response.response_time) 
                / stats["requests"]
            )
    
    def get_provider_stats(self) -> Dict[str, Any]:
        """Get statistics for all providers"""
        return {
            provider.value: {
                "requests": stats["requests"],
                "success_rate": stats["successes"] / max(stats["requests"], 1),
                "avg_response_time": round(stats["avg_response_time"], 3)
            }
            for provider, stats in self.provider_stats.items()
        }
    
    def get_best_provider_for_task(self, task_type: str) -> LLMProvider:
        """Recommend best provider based on task type and current stats"""
        if task_type in ["complex_reasoning", "planning", "narrative"]:
            return LLMProvider.GROQ
        elif task_type in ["quick_response", "dialogue", "simple_decision"]:
            return LLMProvider.CEREBRAS
        else:
            # Choose based on success rate and response time
            best_provider = LLMProvider.GROQ
            best_score = 0

            for provider, stats in self.provider_stats.items():
                if stats["requests"] > 0:
                    success_rate = stats["successes"] / stats["requests"]
                    response_time_score = 1.0 / (1.0 + stats["avg_response_time"])
                    score = success_rate * 0.7 + response_time_score * 0.3

                    if score > best_score:
                        best_score = score
                        best_provider = provider

            return best_provider

# Global LLM service instance
llm_service = LLMService()
