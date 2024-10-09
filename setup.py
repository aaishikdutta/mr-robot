from setuptools import setup, find_packages

setup(
    name='mr-robot',
    packages=find_packages(),
    version='0.2.0',
    install_requires=[
        'openai',
        'click',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'mr-robot = mr_robot.app:cli',
        ],
    },
)