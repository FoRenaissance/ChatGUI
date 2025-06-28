import cfg.config as config
from agent.gpt_agent import GPTAgent
from agent.gemini_agent import GeminiAgent
from agent.deepseek_agent import DeepseekAgent

model_dict = {
    "ChatGPT": lambda: GPTAgent(type="gpt-4o-mini"),
    "Deepseek-V3": lambda : DeepseekAgent(type="deepseek-chat"),
    "Deepseek-R1": lambda : DeepseekAgent(type="deepseek-reasoner"),
    "Gemini-2.0-flash": lambda : GeminiAgent(type="gemini-2.0-flash"),
    "Gemini-2.5-flash": lambda : GeminiAgent(type="gemini-2.5-flash"),
}

class AgentRouter:
    def __init__(self, ui, current_model):
        self.ui = ui
        self.current_model = current_model
        self.current_agent = model_dict[current_model]()
        
    def switch_model(self, new_model):
        if new_model!=self.current_model and new_model in model_dict:
            self.current_model = new_model
            del self.current_agent
            self.current_agent = model_dict[new_model]()
        
    def route_return(self, msg):
        agent_reply = self.current_agent.send_message(msg)
        return agent_reply
    
    def before_route(self):
        if not hasattr(config, f"{self.current_model.split('-')[0]}_API_KEY") or not getattr(config, f"{self.current_model.split('-')[0]}_API_KEY", ""):
            self.ui.show_setting()
            return False
        return True