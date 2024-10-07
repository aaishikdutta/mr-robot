# Mr. Robot CLI

## Overview

Mr. Robot is a tiny command-line interface (CLI) application that utilizes OpenAI's language models to generate and execute shell commands based on user queries.

## Requirements

- Python 3.8 or newer
- OpenAI API key

## How to use?

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/mr-robot.git
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
CopyUsage: mr-robot [OPTIONS]

Options:
  -a, --api-key TEXT              API key for openai API. If not added will
                                  look for env variable 'OPENAI_API_KEY'
  -d, --script-dir TEXT           Specify the directory to store the generated
                                  scripts  [default: /home/pi/.mr-robot]
  -m, --model-name TEXT           openai model name.  [default: gpt-4o-mini]
  -o, --os TEXT                   name of the target os that would run the
                                  commands
  -p, --permission-mode [all|none|sudo]
  -s, --shell TEXT                name of the target shell that would execute
                                  the commands
  --version                       Show the version and exit.
  --help                          Show this message and exit.


