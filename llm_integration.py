import os
import requests
import json
import time
import random
from transformers import pipeline

# Choose which LLM implementation to use
# Options: 'local', 'huggingface', 'ollama'
LLM_IMPLEMENTATION = 'local'  # Change this based on your preference

class LLMInterface:
    """Interface for different LLM implementations"""
    
    def generate_text(self, prompt, max_length=300):
        """Generate text based on the prompt"""
        raise NotImplementedError("Subclasses must implement generate_text")

class LocalLLM(LLMInterface):
    """Uses local transformers library with a smaller model"""
    
    def __init__(self, model_name="gpt2"):
        self.generator = pipeline('text-generation', model=model_name)
    
    def generate_text(self, prompt, max_length=300):
        result = self.generator(prompt, max_length=max_length, num_return_sequences=1)
        return result[0]['generated_text'][len(prompt):]

class HuggingFaceLLM(LLMInterface):
    """Uses Hugging Face Inference API"""
    
    def __init__(self, model_name="gpt2", api_key=None):
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("HUGGINGFACE_API_KEY")
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        
    def generate_text(self, prompt, max_length=300):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": max_length,
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
            }
        }
        
        response = requests.post(self.api_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            
            # Different models return different response formats
            if isinstance(result, list) and len(result) > 0:
                if "generated_text" in result[0]:
                    return result[0]["generated_text"][len(prompt):]
                else:
                    return result[0]
            elif isinstance(result, dict) and "generated_text" in result:
                return result["generated_text"][len(prompt):]
            
            return str(result)
        else:
            # If API call fails, return a placeholder
            print(f"Error: {response.status_code}, {response.text}")
            return f"[Error generating text: {response.status_code}]"

class OllamaLLM(LLMInterface):
    """Uses Ollama local API (https://ollama.ai/)"""
    
    def __init__(self, model_name="llama2"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"
        
    def generate_text(self, prompt, max_length=300):
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": max_length,
            }
        }
        
        try:
            response = requests.post(self.api_url, json=payload)
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "[No response generated]")
            else:
                print(f"Error: {response.status_code}, {response.text}")
                return f"[Error generating text: {response.status_code}]"
        except Exception as e:
            print(f"Exception when calling Ollama: {e}")
            return "[Error connecting to Ollama. Is it running?]"

class FallbackLLM(LLMInterface):
    """Simple rule-based fallback when no LLM is available"""
    
    def __init__(self):
        # Pre-defined responses for different scenarios
        self.introductions = [
            "You find yourself in a mysterious land filled with magic and danger. The air smells of adventure, and your journey begins now.",
            "The kingdom of Eldoria welcomes you, brave adventurer. Dark forces are stirring, and only you can stop them.",
            "As you awaken in the small village of Meadowbrook, you sense something is wrong. The normally bustling streets are quiet."
        ]
        
        self.locations = {
            "village": [
                "The village is small but lively. Villagers go about their daily tasks, occasionally giving you curious glances.",
                "A quaint village with thatched roofs and cobblestone streets. A blacksmith hammers away at his forge.",
                "The village square is bustling with activity. A market is in full swing, with vendors calling out to passersby."
            ],
            "forest": [
                "Tall trees block out most of the sunlight, creating an eerie atmosphere. You hear rustling in the undergrowth.",
                "The forest is dense and ancient. Moss-covered trees stretch as far as the eye can see.",
                "A mist hangs between the trees, limiting visibility. Strange sounds echo from all directions."
            ],
            "castle": [
                "The castle looms above you, its stone walls weathered by time. Guards stand at attention at the entrance.",
                "A magnificent castle with tall spires and colorful banners fluttering in the wind.",
                "The castle courtyard is busy with knights training and servants hurrying about their duties."
            ],
            "cave": [
                "The cave entrance is dark and foreboding. A cool breeze carries strange odors from within.",
                "Stalactites hang from the ceiling of the cave, some dripping water into small pools below.",
                "The cave walls glitter with mineral deposits, occasionally catching the light from your torch."
            ],
            "tavern": [
                "The tavern is warm and inviting. The smell of ale and roasted meat fills the air.",
                "A rowdy tavern filled with adventurers sharing tales of their exploits.",
                "The tavern keeper eyes you suspiciously as you enter. A group of patrons in the corner fall silent."
            ]
        }
        
        self.encounters = [
            "A strange figure approaches you. They seem friendly, but there's something off about their smile.",
            "You hear a rustling in the bushes. Suddenly, a goblin leaps out, brandishing a crude dagger!",
            "A merchant's cart has broken down on the road. The merchant calls out to you for help.",
            "You find a mysterious chest partially buried in the ground. It doesn't appear to be locked.",
            "A group of travelers invite you to join them around their campfire for the night."
        ]
        
        self.combat_results = [
            "You engage in combat! After a fierce struggle, you emerge victorious, though somewhat wounded.",
            "Your opponent strikes first, catching you off guard. You take damage but manage to defeat them.",
            "Using your skills and quick thinking, you defeat your enemy without taking any damage.",
            "The battle is intense but brief. You overpower your opponent, though not without cost."
        ]
        
        self.discoveries = [
            "You find a small pouch containing gold coins hidden beneath a loose floorboard.",
            "Among the defeated enemy's possessions, you discover a strange amulet that seems to pulse with magical energy.",
            "A dusty book on a forgotten shelf catches your eye. It contains information about ancient ruins nearby.",
            "You stumble upon a hidden cache of supplies, including healing potions and ammunition."
        ]
    
    def generate_text(self, prompt, max_length=300):
        # Simple keyword matching to determine context
        prompt_lower = prompt.lower()
        
        # Introduction generation
        if "introduction" in prompt_lower or "begin" in prompt_lower or "start" in prompt_lower:
            return random.choice(self.introductions)
        
        # Location descriptions
        for location, descriptions in self.locations.items():
            if location in prompt_lower:
                return random.choice(descriptions)
        
        # Random encounters
        if "encounter" in prompt_lower or "meet" in prompt_lower or "find" in prompt_lower:
            return random.choice(self.encounters)
        
        # Combat results
        if "fight" in prompt_lower or "battle" in prompt_lower or "attack" in prompt_lower or "combat" in prompt_lower:
            return random.choice(self.combat_results)
        
        # Discoveries
        if "search" in prompt_lower or "look" in prompt_lower or "examine" in prompt_lower:
            return random.choice(self.discoveries)
        
        # Default response for other scenarios
        return "You continue on your adventure, alert for any dangers or opportunities that might present themselves."

# Factory function to get the appropriate LLM implementation
def get_llm():
    if LLM_IMPLEMENTATION == 'local':
        try:
            return LocalLLM()
        except Exception as e:
            print(f"Failed to initialize local LLM: {e}")
            print("Falling back to rule-based generation")
            return FallbackLLM()
    
    elif LLM_IMPLEMENTATION == 'huggingface':
        api_key = os.environ.get("HUGGINGFACE_API_KEY")
        if not api_key:
            print("No Hugging Face API key found. Set the HUGGINGFACE_API_KEY environment variable.")
            print("Falling back to rule-based generation")
            return FallbackLLM()
        
        return HuggingFaceLLM(model_name="gpt2", api_key=api_key)
    
    elif LLM_IMPLEMENTATION == 'ollama':
        return OllamaLLM()
    
    else:
        print(f"Unknown LLM implementation: {LLM_IMPLEMENTATION}")
        print("Falling back to rule-based generation")
        return FallbackLLM()
