from agent.base_agent import BaseAgent
import cfg.config as config

class GPTAgent(BaseAgent):
    
    def __init__(self, type):
        super().__init__(type)

    def _setup_config(self):
        self.temperature = getattr(config, f"ChatGPT_TEMEPERATURE", 0.7)
        self.max_completion_tokens = getattr(config, f"ChatGPT_MAX_TOKENS", 2048)
        self.api_key = getattr(config, f"ChatGPT_API_KEY", "")
        self.base_url = "https://api.openai.com/v1"