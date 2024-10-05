import os
import uuid

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

def get_default_system_prompt(os_info = 'Linux', os_arch = 'i386', shell = '/bin/bash'):
    shell_name = shell.split('/')[-1] 

    system_propmt = f"""You are an advanced coding translator. You take natural language input and translate it directly into valid {shell_name} commands for {os_info} {os_arch}. Avoid using unnecessary escape characters (e.g., `\\n` and `\\"`), and ensure the script is clean and executable in a standard terminal. If a user asks to generate a file, return the correct `cat` or `echo` command without escaping the content. Output only the commands without explanations."""
    return system_propmt

def get_default_base_directory():
    return os.path.join(os.path.expanduser('~'), '.mr-robot')

def create_execution_script(base_dir, content):

    base_dir = os.path.join(base_dir, 'mr-robot-exec-scripts')
    
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    if not content:
        return None
    
    file_name = base_dir + '/' + str(uuid.uuid4()) + '.sh'
    perm = 0o755
    with open(file_name, 'w+') as f:
        f.write(content)
    os.chmod(file_name, perm)
    return file_name

def remove_execution_scripts(base_dir):
    base_dir = os.path.join(base_dir, 'mr-robot-exec-scripts')
    if os.path.exists(base_dir):
        for item in os.listdir(base_dir):
            item_path = os.path.join(base_dir, item)
            if os.path.isfile(item_path):
                os.remove(item_path)


