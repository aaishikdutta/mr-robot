# Mr. Robot CLI

## Overview

Mr. Robot is a tiny command-line interface (CLI) application that utilizes OpenAI's language models to generate and execute shell commands based on user queries.

## Requirements

- Python 3.8 or newer
- OpenAI API key

## How to use?

1. Clone the repository:
   ```
   git clone https://github.com/aaishikdutta/mr-robot.git
   ```

2. Create a new environment (using conda):
   ```
   conda create --name mr-robot-env python=3.11
   conda activate mr-robot-env
   ```

3. Install dependency:
   ```
   pip install -e .
   ```

4. Add OpenAI API key:
   ```
   export OPENAI_API_KEY='your-openai-api-key'
   ```

5. Run mr-robot in CLI:
   ```
   mr-robot
   ```

## CLI Options

Mr. Robot CLI supports several command-line options to customize its behavior:

```
Usage: mr-robot [OPTIONS]

Options:
  -a, --api-key TEXT              API key for OpenAI API. If not added, will
                                  look for env variable 'OPENAI_API_KEY'
  -d, --script-dir TEXT           Specify the directory to store the generated
                                  scripts  [default: /home/pi/.mr-robot]
  -m, --model-name TEXT           OpenAI model name  [default: gpt-4o-mini]
  -o, --os TEXT                   Name of the target OS that would run the
                                  commands
  -p, --permission-mode [all|none|sudo]
                                  Set the permission mode for command execution
  -s, --shell TEXT                Name of the target shell that would execute
                                  the commands
  --version                       Show the version and exit
  --help                          Show this message and exit
```

Examples:

1. Use Mr. Robot with a specific API key:
   ```
   mr-robot -a "your-api-key-here"
   ```

2. Specify a custom directory for generated scripts:
   ```
   mr-robot -d "/path/to/custom/directory"
   ```

3. Use a different OpenAI model:
   ```
   mr-robot -m "gpt-3.5-turbo"
   ```

4. Specify the target operating system:
   ```
   mr-robot -o "ubuntu"
   ```

5. Set a specific permission mode:
   ```
   mr-robot -p sudo
   ```

6. Specify the target shell:
   ```
   mr-robot -s "bash"
   ```




