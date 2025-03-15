from typing import Dict, Any, Optional
import logging
import os
from openai import AsyncOpenAI
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogAnalyzer:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.mistral_tokenizer = None
        self.mistral_model = None
        
    async def init_mistral(self):
        """Initialize Mistral model if not already loaded."""
        if self.mistral_model is None:
            self.mistral_tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
            self.mistral_model = AutoModelForCausalLM.from_pretrained(
                "mistralai/Mistral-7B-v0.1",
                torch_dtype=torch.float16,
                device_map="auto"
            )

    async def analyze_with_gpt4(self, log_content: str) -> Dict[str, Any]:
        """Analyze log content using GPT-4."""
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity log analyzer. Analyze the following log entry and provide insights about potential security threats."},
                    {"role": "user", "content": log_content}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            return {
                "analysis": response.choices[0].message.content,
                "model": "gpt-4",
                "confidence": response.choices[0].finish_reason == "stop"
            }
        except Exception as e:
            logger.error(f"Error in GPT-4 analysis: {str(e)}")
            raise

    async def analyze_with_mistral(self, log_content: str) -> Dict[str, Any]:
        """Analyze log content using Mistral-7B."""
        try:
            await self.init_mistral()
            
            inputs = self.mistral_tokenizer(
                f"Analyze this security log and identify potential threats: {log_content}",
                return_tensors="pt",
                max_length=512,
                truncation=True
            ).to("cuda")
            
            with torch.no_grad():
                outputs = self.mistral_model.generate(
                    **inputs,
                    max_new_tokens=200,
                    temperature=0.3,
                    do_sample=True
                )
            
            analysis = self.mistral_tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return {
                "analysis": analysis,
                "model": "mistral-7b",
                "confidence": True  # Simplified confidence measure
            }
        except Exception as e:
            logger.error(f"Error in Mistral analysis: {str(e)}")
            raise

    async def analyze_log(self, log_content: str, model: str = "gpt4") -> Dict[str, Any]:
        """Main method to analyze logs with specified model."""
        try:
            if model.lower() == "gpt4":
                return await self.analyze_with_gpt4(log_content)
            elif model.lower() == "mistral":
                return await self.analyze_with_mistral(log_content)
            else:
                raise ValueError(f"Unsupported model: {model}")
        except Exception as e:
            logger.error(f"Error in log analysis: {str(e)}")
            raise