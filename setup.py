from setuptools import setup

setup(
    name='mr-robot',
    version='0.1.0',
    py_modules=['app'],
    install_requires=[
        'openai',
        'click',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'mr-robot = app:hello',
        ],
    },
)