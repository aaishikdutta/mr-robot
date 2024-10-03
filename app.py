import click
import platform
import os

from rich.console import Console
from misc.util import print_init, get_default_tool, get_default_system_prompt
from core.model import Model
from core.tool import Tool


os_info = platform.system()
os_arch = platform.machine()
shell = os.getenv('SHELL', 'Unknown')

console = Console()
model = Model(tools=get_default_tool(os_info, os_arch, shell))
tool = Tool()

def hello():
    print_init(console, os_info, os_arch, shell)
    
    while True:
        value = click.prompt(click.style("∆", fg=(244, 143, 177), bold=True))
        # exit if user types '/kill'
        if value == '/kill':
            break

        

        # TODO: allow user to have option to add their own system prompts. 
        # They can either save it in some file or they can add it as a string while calling the cli
        sys_prompt = get_default_system_prompt(os_info, os_arch, shell)

        # generate completions based on user input
        commands = model.generate_completions(sys_prompt, value, tool_key="commands")
        if not commands:
            break

        console.print('\n[#F48FB1 bold]Mr. Robot:[/#F48FB1 bold] \n'
                      f"{commands}\n" , style="#9575CD")
        
        confirm = click.prompt(click.style('Run Script? [Yes, No]', fg=(244, 143, 177), bold=True))
        if len(confirm) > 0:
            if confirm[0].lower() == 'n':
                continue
        
        
        output = tool.execute_commands(commands)
        console.print('\n[#F48FB1 bold]ø:[/#F48FB1 bold] \n'
                      f"{output.decode('utf-8')}", style="#9575CD")
    
    

        


        

        
        
