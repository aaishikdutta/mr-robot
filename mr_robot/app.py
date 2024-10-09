import click
import platform
import os

from importlib.metadata import version

from rich.console import Console

from .misc.util import get_default_system_prompt, get_default_base_directory, remove_execution_scripts, get_commands_help
from .misc.constants import ASCII_LOGO

from .core.model import Model


os_info = platform.system()
os_arch = platform.machine()
env_shell = os.getenv('SHELL', 'Unknown').split('/')[-1]

console = Console()


@click.command()
@click.option('-a', '--api-key', envvar='OPENAI_API_KEY', help="API key for openai API. If not added will look for env variable 'OPENAI_API_KEY'")
@click.option('-d', '--script-dir', default=get_default_base_directory(), show_default=True, help='Specify the directory to store the generated scripts')
@click.option('-m', '--model-name', default="gpt-4o-mini", show_default=True, help="openai model name.")
@click.option('-o', '--os', default=f"{os_info} {os_arch}", help="name of the target os that would run the commands")
@click.option('-p', '--permission-mode', type=click.Choice(['all', 'none', 'sudo'], case_sensitive=False), default="all")
@click.option('-s', '--shell', default=env_shell, help="name of the target shell that would execute the commands")
@click.version_option(package_name="mr-robot")
def cli(api_key, permission_mode, script_dir, model_name, os, shell):
    try:
        # basic cli greeting and stuff
        console.print(ASCII_LOGO, style="#B39DDB")
        console.print(
            '\n[#B39DDB bold]---------------------------------------------[/#B39DDB bold]\n'
            '[#B39DDB bold]Mr. Robot:[/#B39DDB bold] Language based System Admin '
            f'[#F48FB1 bold]{version("mr-robot")}[/#F48FB1 bold]\n'
            f'[#B39DDB bold]OS:[/#B39DDB bold] [bold]{os}[/bold]\n'
            f'[#B39DDB bold]Shell:[/#B39DDB bold] [bold]{shell}[/bold]\n'
            '[#B39DDB bold]---------------------------------------------[/#B39DDB bold]\n',
            style="#F48FB1"
        )
        console.print(
            "[#F48FB1 bold]ø:[/#F48FB1 bold] Provide sudo password", style="#B39DDB")
        sudo_password = click.prompt(click.style(
            "∆", fg=(244, 143, 177), bold=True), hide_input=True)

        console.print(
            "\n[#F48FB1 bold]ø:[/#F48FB1 bold] Send a query after ∆ ('/?' for help) \n", style="#B39DDB")

        model = Model(cli=shell, os=os, model_name=model_name, api_key=api_key)

        while True:

            value = click.prompt(click.style(
                "∆", fg=(244, 143, 177), bold=True))
            # exit if user types '/kill'
            if value == '/kill':
                break

            elif value == '/clear':
                # clear scripts and context
                remove_execution_scripts(base_dir=script_dir)
                continue

            elif value == '/?':
                table = get_commands_help()
                console.print('\n\n', table, '\n\n')
                continue

            # TODO: allow user to have option to add their own system prompts.
            # They can either save it in some file or they can add it as a string while calling the cli
            sys_prompt = get_default_system_prompt(os, shell)

            # generate completions based on user input
            # this is essentially a dictionary of all parameters returned by the function calling model
            arguments = model.generate_completions(sys_prompt, value)
            if not arguments:
                console.print(
                    '\n[#F48FB1 bold]ø:[/#F48FB1 bold] No script returned by mr-robot.', style="#9575CD")
                continue

            # show command and ask for permission to run if only permission mode is `all`
            # check if the generated script has `sudo` in it to ask for permission if permission mode is 'sudo'
            # directly execute if permission mode is `none`
            commands = arguments[model.tool_key]
            is_sudo_script = 'sudo' in commands

            if permission_mode == 'all' or (permission_mode == 'sudo' and is_sudo_script):
                console.print('\n[#F48FB1 bold]Mr. Robot:[/#F48FB1 bold] \n'
                              f"{arguments[model.tool_key]}\n", style="#9575CD")

                console.print(
                    "[#F48FB1 bold]ø:[/#F48FB1 bold] Run Script? (Y/n)", style="#B39DDB")
                confirm = click.confirm(click.style(
                    '∆', fg=(244, 143, 177), bold=True))
                
                if not confirm:
                    continue

            output = model.execute_commands(script_dir, sudo_password, **arguments)
            console.print('\n[#F48FB1 bold]ø:[/#F48FB1 bold] \n'
                          f"{output}", style="#9575CD")

    except Exception as e:
        console.print(f'{e}', style="#E57373")
