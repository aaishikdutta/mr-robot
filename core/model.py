import json
import os
import pexpect
import platform

from misc.util import create_execution_script
from openai import OpenAI

shell = os.getenv('SHELL', 'Unknown')
shell_name = shell.split('/')[-1] 
os_info = platform.system()
os_arch = platform.machine()

class Model:

    def __init__(self, model, api_key=None ):

        if not api_key:
            raise ValueError("Openai API key not found! Please add the API key either by setting the 'OPENAI_API_KEY' environment variable or by passing the api-key using the '--api-key' option while calling mr-robot")
        
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.tool = [{
            "type": "function",
            "function": {
                "name": "get_script",
                "description": f"Generate and return valid {shell_name} commands that can be executed directly in a terminal without escape sequences.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commands": {
                        "type": "string",
                        "description": f"A valid {shell_name} command generated from the user query, which should be executable in a {os_info} {os_arch} terminal without unnecessary escape characters."
                        }
                    },
                "required": ["commands"],
                "additionalProperties": False
                }
            }
        }]
        self.tool_key = "commands"

    def generate_completions(self, system_prompt = "", user_input = ""):

        if not user_input or not system_prompt:
            raise ValueError("Value for 'user_input' and/or 'system_prompt' missing.")
        
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
            tools=self.tool
        )
        response = completions.choices[0].message.tool_calls[0].function.arguments
        response_arguments = json.loads(response)

        return response_arguments
    
    def execute_commands(self, base_dir, **arguments):

        if self.tool_key not in arguments:
            raise ValueError(f"Missing required argument: {self.tool_key}")

        commands = arguments[self.tool_key]
        content = f'#!{shell}\n\n' + commands
        script_path = create_execution_script(base_dir, content)
        
        if not script_path:
            return None
        
        # TODO: add finer control to process creation
        output = pexpect.run(f'{shell_name} {script_path}')
        return output.decode('utf-8')
            

    
