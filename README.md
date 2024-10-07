# Mr. Robot CLI

## Overview

Mr. Robot is a tiny command-line interface (CLI) application that utilizes OpenAI's language models to generate and execute shell commands based on user queries.

## How to use?

Clone the repository:
```git clone https://github.com/yourusername/mr-robot.git```

Create a new environment (I used conda):
```conda create --name mr-robot-env python=3.11```
```conda activate mr-robot-env```

Install dependency:
```pip install -e .```

Add openai api key:
```export OPENAI_API_KEY='your-openai-api-key'```

Run mr-robot in cli:
```mr-robot```

