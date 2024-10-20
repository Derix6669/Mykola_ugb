from openai import OpenAI
from AI.app_state import State, Config
from AI.backend.prompts import Prompt


class Client:
    """
    Client class to interact with the OpenAI GPT-4 API using predefined prompts.

    Attributes:
        client (OpenAI): The OpenAI API client initialized with the API key.
    """

    def __init__(self):
        """
        Initializes the Client instance with the OpenAI API key from the configuration.
        """
        self.client = OpenAI(api_key=Config.API_KEY)

    def __send_prompt(self, prompt: str) -> str:
        """
        Sends a prompt to the OpenAI GPT-4 API and retrieves the response.

        Args:
            prompt (str): The prompt to send to the GPT-4 model.

        Returns:
            str: The text content of the model's response.
        """
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
        print(response_text)  # Optional logging, can be removed if not needed
        return response_text

    def __get_response(self, text: str, task_name: str) -> str:
        """
        Retrieves the response from the OpenAI API based on the task name and input text.

        Args:
            task_name (str): The name of the task (e.g., 'category_definition', 'finding_common_context').
            text (str): The text that will be processed by the model.

        Raises:
            ValueError: If the task name does not match any known prompt.

        Returns:
            str: The response from the OpenAI API.
        """
        # Construct the prompt key dynamically
        prompt_key = f"{task_name.upper()}_PROMPT"

        # Retrieve the corresponding prompt from the Prompt class
        prompt = getattr(Prompt, prompt_key, None)

        if not prompt:
            raise ValueError(f"Unknown request type: {task_name}")

        # Send the prompt to the model and return the response
        response = self.__send_prompt(prompt.format(text=text))
        return response

    def __call__(self, task_name: str, text: str, *args, **kwargs) -> str:
        """
        Calls the client to get a response for a given task and text.

        Args:
            task_name (str): The task to be performed (e.g., 'category_definition').
            text (str): The input text for the task.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The response text from the OpenAI API.
        """
        return self.__get_response(text, task_name)


# Instantiate the client for use
client = Client()
