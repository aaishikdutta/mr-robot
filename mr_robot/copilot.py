import os
import platform
import sys

from mr_robot.core.model import Model
from mr_robot.misc.util import get_default_system_prompt

def main():
    try:

        os_info = platform.system()
        os_arch = platform.machine()
        env_shell = os.getenv('SHELL', 'Unknown').split('/')[-1]
        api_key = os.getenv("OPENAI_API_KEY", "")

        model = Model(cli=env_shell, os=f"{os_info} {os_arch}", model_name="gpt-4o-mini", api_key=api_key)

        sys_prompt = get_default_system_prompt(os=f"{os_info} {os_arch}", shell=env_shell)
        user_input = sys.argv[1]

        arguments = model.generate_completions(sys_prompt, user_input)
        print(arguments[model.tool_key])
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__== "__main__":
    main()

