import os
import uuid

from rich import box
from rich.table import Table

# return the help
def get_commands_help():
    table = Table(title="[#B39DDB]Available commands[/#B39DDB]",
                  box=box.ASCII_DOUBLE_HEAD, style="#B39DDB")
    table.add_column("[#9575CD]command[/#9575CD]", justify="left")
    table.add_column(
        "[#9575CD]description[/#9575CD]", justify="left")
    table.add_row("[#B39DDB]/kill[/#B39DDB]",
                  "Exit mr-robot", style="#F48FB1")
    table.add_row("[#B39DDB]/clear[/#B39DDB]",
                  "Remove execution scripts", style="#F48FB1")
    
    return table


def get_default_system_prompt(os='Linux', shell='bash'):

    system_propmt = f"""You are an advanced coding translator. You take natural language input and translate it directly into valid {shell} commands for {os}. Avoid using unnecessary escape characters (e.g., `\\n` and `\\"`), and ensure the script is clean and executable in a standard terminal. If a user asks to generate a file, return the correct `cat` or `echo` command without escaping the content. Output only the commands without explanations."""
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
