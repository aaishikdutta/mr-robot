import click
import platform
import os

from rich.console import Console
from misc.util import print_init, get_default_system_prompt, get_base_directory
from core.model import Model


os_info = platform.system()
os_arch = platform.machine()
shell = os.getenv('SHELL', 'Unknown')

console = Console()

@click.command()
@click.option('-m', '--model', default="gpt-4o-mini", show_default=True, help="openai model name.")
@click.option('-d', '--script-dir', default=get_base_directory(), show_default=True, help='Specify the directory to store the generated scripts')
@click.option('--api-key', envvar='OPENAI_API_KEY', help="API key for openai API. If not added will look for env variable 'OPENAI_API_KEY'")
@click.version_option(package_name="mr-robot")
def cli(model, script_dir, api_key):
    try:
        print_init(console, os_info, os_arch, shell)
        model = Model(model, api_key=api_key)
    
        while True:
            value = click.prompt(click.style("∆", fg=(244, 143, 177), bold=True))
            # exit if user types '/kill'
            if value == '/kill':
                break

            # TODO: allow user to have option to add their own system prompts. 
            # They can either save it in some file or they can add it as a string while calling the cli
            sys_prompt = get_default_system_prompt(os_info, os_arch, shell)

            # generate completions based on user input
            # this is essentially a dictionary of all parameters returned by the function calling model
            arguments = model.generate_completions(sys_prompt, value)
            if not arguments:
                break

            console.print('\n[#F48FB1 bold]Mr. Robot:[/#F48FB1 bold] \n'
                        f"{arguments[model.tool_key]}\n" , style="#9575CD")
            
            confirm = click.prompt(click.style('Run Script? [Yes, No]', fg=(244, 143, 177), bold=True))
            if len(confirm) > 0:
                if confirm[0].lower() == 'n':
                    continue
            
            
            output = model.execute_commands(script_dir, **arguments)
            console.print('\n[#F48FB1 bold]ø:[/#F48FB1 bold] \n'
                        f"{output}", style="#9575CD")
    
    except Exception as e:
        console.print(f'[bold]Error![/bold] {e}', style="#E57373")

    
    

        


        

        
        
