import json

from collections import Iterable

from openai import OpenAI
from openai.types.chat import ChatCompletionToolParam, ChatCompletionMessage

class Model:

    def __init__(self, model = 'gpt-4o-mini', tools:Iterable[ChatCompletionToolParam] = None ):
        # TODO: handle api key env stuff
        self.client = OpenAI()
        self.model = model
        self.tools = tools

    def generate_completions(self, system_prompt = "", user_input = "", tool_key = ""):
        try:
            if not user_input or not system_prompt or not tool_key:
                raise ValueError("Value for `user_input`, `system_prompt` and/or `tool_key` missing.")
            
            completions = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                tools=self.tools
            )
            response = completions.choices[0].message.tool_calls[0].function.arguments
            response_arguments = json.loads(response)

            return response_arguments[tool_key]
            
        except ValueError as e:
            print(e)
            return None

        except:
            print("Something Went Wrong!")
            return None

    
