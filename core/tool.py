import os
import uuid
import pexpect

class Tool:
    def __init__(self,  base_dir:str = None):
        default_base_dir = os.path.join(os.path.expanduser('~'), '.mr-robot', 'scripts')
        if not base_dir:
            self.base_dir = default_base_dir
        else:
            self.base_dir = base_dir 

    # TODO: extend this method to let user create scripts to be used at a later time
    def create_script(self, commands):
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        if not commands:
            return None

        file_name = self.base_dir + '/' + str(uuid.uuid4()) + '.sh'
        content = '#!/bin/bash\n\n' + commands
        perm = 0o755
        with open(file_name, 'w+') as f:
            f.write(content)
        os.chmod(file_name, perm)
        return file_name
    
    def execute_commands(self, commands):
        script_path = self.create_script(commands)
        
        if not script_path:
            return None
        
        # TODO: add finer control to process creation
        output = pexpect.run(f'bash {script_path}')
        return output
