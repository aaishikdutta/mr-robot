from setuptools import setup, find_packages

setup(
    name='mr-robot',
    packages=find_packages(),
    version='0.1.2',
    py_modules=['app'],
    install_requires=[
        'openai',
        'click',
        'rich',
        'pexpect'
    ],
    entry_points={
        'console_scripts': [
            'mr-robot = app:cli',
        ],
    },
)