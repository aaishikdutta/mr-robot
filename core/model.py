import json, subprocess

from misc.util import create_execution_script
from openai import OpenAI

class Model:

    def __init__(self, cli, os, model_name, api_key=None ):

        if not api_key:
            raise ValueError("Openai API key not found! Please add the API key either by setting the 'OPENAI_API_KEY' environment variable or by passing the api-key using the '--api-key' option while calling mr-robot")
        
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
        self.cli = cli
        self.os = os
        self.tool = [{
            "type": "function",
            "function": {
                "name": "get_script",
                "description": f"Generate and return valid {cli} commands that can be executed directly in a terminal without escape sequences.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commands": {
                        "type": "string",
                        "description": f"A valid {cli} command generated from the user query, which should be executable in a {os} terminal without unnecessary escape characters."
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
            model=self.model_name,
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
            tools=self.tool,
            parallel_tool_calls=False
        )

        response = completions.choices[0].message

        # handle case where model won't use tool call
        if not response.tool_calls:
            return None
        
        # extract json parameters returned by model

        response_arguments = json.loads(response.tool_calls[0].function.arguments)
        return response_arguments
    
    def execute_commands(self, base_dir, sudo_password, **arguments):
        if self.tool_key not in arguments:
            raise ValueError(f"Missing required argument: {self.tool_key}")

        commands = arguments[self.tool_key]
        content = f'#!/bin/bash\n\n' + commands
        script_path = create_execution_script(base_dir, content)
        
        if not script_path:
            return None
        
        # Prepare the base command
        command = ['bash', script_path]

        if 'sudo' in commands:
            # If the command requires sudo, we prepend sudo and use -S to accept password from stdin
            command = ['sudo', '-S'] + command

        try:
            # Start the process
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,   # To send the sudo password if needed
                stdout=subprocess.PIPE,  # To capture stdout
                stderr=subprocess.PIPE,  # To capture stderr
                text=True                # Enable text mode to work with strings instead of bytes
            )

            # If sudo is in the command, pass the password
            if 'sudo' in commands:
                stdout, stderr = process.communicate(input=sudo_password + '\n')
            else:
                stdout, stderr = process.communicate()

            if process.returncode != 0:
                return f"Error: {stderr}"
            
            return stdout

        except Exception as e:
            return f"Execution failed: {str(e)}"

            

    
