from agent.base_agent import BaseAgent
import cfg.config as config

class DeepseekAgent(BaseAgent):
    def __init__(self, type):
        super().__init__(type)

    def _setup_config(self):
        self.temperature = getattr(config, "Deepseek_TEMPERATURE", 1.3)
        self.max_completion_tokens = getattr(config, "Deepseek_MAX_TOKENS", 2048)
        self.api_key = getattr(config, 'Deepseek_API_KEY', "")
        self.base_url = "https://api.deepseek.com"