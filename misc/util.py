import os

from importlib.metadata import version
from misc.constants import ASCII_LOGO
from rich.console import Console



def print_init(console: Console, os_info = 'Linux', os_arch = 'i386', shell = '/bin/bash'):
    shell_name = shell.split('/')[-1] 

    console.print(ASCII_LOGO, style="#B39DDB")
    console.print(
    '\n[#B39DDB bold]---------------------------------------------[/#B39DDB bold]\n'
    '[#B39DDB bold]Mr. Robot:[/#B39DDB bold] Language based System Admin '
    f'[#F48FB1 bold]{version("mr-robot")}[/#F48FB1 bold]\n'
    f'[#B39DDB bold]OS:[/#B39DDB bold] [bold]{os_info} {os_arch}[/bold]\n'
    f'[#B39DDB bold]Shell:[/#B39DDB bold] [bold]{shell_name}[/bold]\n'
    '[#B39DDB bold]---------------------------------------------[/#B39DDB bold]\n',
    style="#F48FB1"
    )
    # console.print("[#F48FB1 bold]ø:[/#F48FB1 bold] Type [italics]'/kill'[/italics] to exit! \n", style="#C2185B")

def get_default_system_prompt(os_info = 'Linux', os_arch = 'i386', shell = '/bin/bash'):
    shell_name = shell.split('/')[-1] 

    system_propmt = f"""You are an advanced coding translator. You take natural language input and translate it directly into valid {shell_name} commands for {os_info} {os_arch}. Avoid using unnecessary escape characters (e.g., `\\n` and `\\"`), and ensure the script is clean and executable in a standard terminal. If a user asks to generate a file, return the correct `cat` or `echo` command without escaping the content. Output only the commands without explanations."""
    return system_propmt

def get_base_directory():
    return os.path.join(os.path.expanduser('~'), '.mr-robot', 'scripts')