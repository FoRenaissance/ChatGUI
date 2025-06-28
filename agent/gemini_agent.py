from agent.base_agent import BaseAgent
import cfg.config as config

class GeminiAgent(BaseAgent):    
    def __init__(self, type):
        super().__init__(type)

    def _setup_config(self):
        self.temperature = getattr(config, 'Gemini_TEMPERATURE',0.7)
        self.max_completion_tokens = getattr(config, 'Gemini_MAX_TOKENS', 2048)
        self.api_key = getattr(config, "Gemini_API_KEY", "")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"