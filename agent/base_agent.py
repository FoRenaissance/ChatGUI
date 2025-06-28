from openai import OpenAI


class BaseAgent:
    def __init__(self, type):
        self.type = type
        self.client = None

    def _setup_config(self):
        raise NotImplementedError

    def _setup_client(self) -> None:
        self._setup_config()
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def send_message(self, message, **kwargs) -> str:
        try:
            self._setup_client()
            response = self.client.chat.completions.create(
                model = self.type,
                messages = [
                    {'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content': message}
                ],
                stream = False,
                temperature = self.temperature,
                max_completion_tokens = self.max_completion_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise e