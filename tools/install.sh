#!/bin/sh

git clone https://github.com/aaishikdutta/mr-robot.git && cd mr-robot

python3 -m venv venv
source venv/bin/activate

pip install -e .

mr-robot
