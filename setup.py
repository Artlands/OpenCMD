from setuptools import setup, find_packages

setup(
    name="opencmd",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai", 
    ],
    entry_points={
        'console_scripts': [
            'opencmd=opencmd.cmd:command_line',  # Replace with your function name
        ],
    },
    include_package_data=True,
)