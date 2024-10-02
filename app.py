import click
import platform
import os
import json
import uuid
import pexpect
import time

from rich.console import Console
from openai import OpenAI

os_info = platform.system()
os_arch = platform.machine()
shell = os.getenv('SHELL', 'Unknown').split('/')[-1]

mr_robot_logo = """\n\n
⣿⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⣛⣛⣛⣛⣛⣛⣛⣛⡛⠛⠛⠛⠛⠛⠛⠛⠛⠛⣿
⣿⠀⠀⠀⠀⢀⣠⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣤⣀⠀⠀⠀⠀⣿
⣿⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⣿
⣿⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⠀⠈⢻⣿⠿⠛⠛⠛⠛⠛⢿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠛⠛⠛⠻⣿⣿⠋⠀⣿
⣿⠛⠁⢸⣥⣴⣾⣿⣷⣦⡀⠀⠈⠛⣿⣿⠛⠋⠀⢀⣠⣾⣿⣷⣦⣤⡿⠈⢉⣿
⣿⢋⣩⣼⡿⣿⣿⣿⡿⠿⢿⣷⣤⣤⣿⣿⣦⣤⣴⣿⠿⠿⣿⣿⣿⢿⣷⣬⣉⣿
⣿⣿⣿⣿⣷⣿⡟⠁⠀⠀⠀⠈⢿⣿⣿⣿⢿⣿⠋⠀⠀⠀⠈⢻⣿⣧⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣥⣶⣶⣶⣤⣴⣿⡿⣼⣿⡿⣿⣇⣤⣴⣶⣶⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⡿⢛⣿⣿⣿⣿⣿⣿⡿⣯⣾⣿⣿⣿⣮⣿⣿⣿⣿⣿⣿⣿⡟⠿⣿⣿⣿
⣿⣿⡏⠀⠸⣿⣿⣿⣿⣿⠿⠓⠛⢿⣿⣿⡿⠛⠛⠻⢿⣿⣿⣿⣿⡇⠀⠹⣿⣿
⣿⣿⡁⠀⠀⠈⠙⠛⠉⠀⠀⠀⠀⠀⠉⠉⠀⠀⠀⠀⠀⠈⠙⠛⠉⠀⠀⠀⣿⣿
⣿⠛⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⠛⣿
⣿⠀⠈⢳⣶⣤⣤⣤⣤⡄⠀⠀⠠⠤⠤⠤⠤⠤⠀⠀⢀⣤⣤⣤⣤⣴⣾⠃⠀⣿
⣿⠀⠀⠈⣿⣿⣿⣿⣿⣿⣦⣀⡀⠀⠀⠀⠀⠀⣀⣤⣾⣿⣿⣿⣿⣿⠇⠀⠀⣿
⣿⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣿
⣿⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⣿
⣿⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠁⠀⠀⠀⠀⣿
⣿⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⣿
⠛⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠛⠛⠛⠉⠉⠛⠛⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠛
⠀⠀⠀⣶⡶⠆⣴⡿⡖⣠⣾⣷⣆⢠⣶⣿⣆⣶⢲⣶⠶⢰⣶⣿⢻⣷⣴⡖⠀⠀
⠀⠀⢠⣿⣷⠂⠻⣷⡄⣿⠁⢸⣿⣿⡏⠀⢹⣿⢸⣿⡆⠀⣿⠇⠀⣿⡟⠀⠀⠀
⠀⠀⢸⣿⠀⠰⣷⡿⠃⠻⣿⡿⠃⠹⣿⡿⣸⡏⣾⣷⡆⢠⣿⠀⠀⣿⠃⠀⠀⠀\n\n\n"""

console = Console()
client = OpenAI()

tools = tools = [{
  "type": "function",
  "function": {
    "name": "get_bash_script",
    "description": "Generate and return valid Bash commands that can be executed directly in a terminal without escape sequences.",
    "parameters": {
      "type": "object",
      "properties": {
        "commands": {
          "type": "string",
          "description": f"A valid {shell} command generated from the user query, which should be executable in a {os_info} {os_arch} terminal without unnecessary escape characters."
        }
      },
      "required": ["commands"]
    }
  }
}]
 
def print_init():
     

    console.print(mr_robot_logo, style="#B39DDB")
    console.print(
    '\n[#B39DDB bold]---------------------------------------------[/#B39DDB bold]\n'
    '[#B39DDB bold]Mr. Robot:[/#B39DDB bold] Language based System Admin '
    '[#F48FB1 bold]v0.1.0[/#F48FB1 bold]\n'
    f'[#B39DDB bold]OS:[/#B39DDB bold] [bold]{os_info} {os_arch}[/bold]\n'
    f'[#B39DDB bold]Shell:[/#B39DDB bold] [bold]{shell}[/bold]\n'
    '[#B39DDB bold]---------------------------------------------[/#B39DDB bold]\n',
    style="#F48FB1"
    )
    console.print("[#F48FB1 bold]ø:[/#F48FB1 bold] Type [italics]'/kill'[/italics] to exit! \n", style="#C2185B")
   

def generate_completions(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"""You are an advanced coding translator. You take natural language input and translate it directly into valid {shell} commands for {os_info} {os_arch}. Avoid using unnecessary escape characters (e.g., `\\n` and `\\"`), and ensure the script is clean and executable in a standard terminal. If a user asks to generate a file, return the correct `cat` or `echo` command without escaping the content. Output only the commands without explanations."""},
            {"role": "user", "content": prompt}
        ],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "get_bash_script"}}
    )

    response = completion.choices[0].message.tool_calls[0].function.arguments
    response_arguments = json.loads(response)

    console.print('[#F48FB1 bold]Mr. Robot:[/#F48FB1 bold] \n'
                  f"{response_arguments['commands']}\n" , style="#9575CD")
    
    return response_arguments['commands']
    

def create_script(bash_script):
    base_dir = os.path.join(os.path.expanduser('~'), '.mr-robot', 'scripts')

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    file_name = base_dir + '/' + str(uuid.uuid4()) + '.sh'
    content = '#!/bin/bash\n\n' + bash_script
    perm = 0o755
    with open(file_name, 'w+') as f:
        f.write(content)
    os.chmod(file_name, perm)
    return file_name




@click.command()
def hello():
    print_init()
    
    while True:
        value = click.prompt(click.style("∆", fg=(244, 143, 177), bold=True))
        # exit if user types '/kill'
        if value == '/kill':
            break

        # generate completions based on user input.
        commands = generate_completions(value)

        confirm = click.prompt(click.style('Run Script? [Yes, No]', fg=(244, 143, 177), bold=True))
        if len(confirm) > 0:
            if confirm[0].lower() == 'n':
                continue
        
        path = create_script(commands)
        # TODO: add finer control to process creation
        output = pexpect.run(f'bash {path}')
        console.print(output)
    
    

        


        

        
        
