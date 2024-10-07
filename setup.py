from setuptools import setup, find_packages

setup(
    name='mr-robot',
    packages=find_packages(),
    version='0.2.0',
    py_modules=['app'],
    install_requires=[
        'openai',
        'click',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'mr-robot = app:cli',
        ],
    },
)