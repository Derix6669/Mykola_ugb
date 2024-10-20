from openai import OpenAI

from AI.app_state import State, Config
from AI.backend.prompts import Prompt


class Client:
    def __init__(self):
        self.client = OpenAI(api_key=Config.API_KEY)

    def __send_prompt(self, prompt: str):

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4",
        )

        response_text = chat_completion.choices[0].message.content
        print(response_text)
        return response_text

    def __get_response(self, text: str, task_name: str) -> str:
        """:param task_name: category_definition, finding_common_context, creating_new_tasks
        :param text: text of the task"""

        prompt_key = f"{task_name.upper()}_PROMPT"
        prompt = getattr(Prompt, prompt_key, None)

        if not prompt:
            raise ValueError(f"Невідомий тип запиту: {task_name}")

        response = self.__send_prompt(prompt.format(text=text))
        return response

    def __call__(self, task_name: str, text: str, *args, **kwargs) -> str:
        return self.__get_response(text, task_name)


client = Client()
