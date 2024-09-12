# OpenCMD

## About OpenCMD
OpenCMD is an intelligent command-line wrapper that integrates a Large Language Model (LLM) to assist users in performing system-related tasks more efficiently. With OpenCMD, users can interact with their system using natural language queries and receive both command recommendations and explanations to simplify complex operations.

## Features
- **Natural Language Processing**: Use everyday language to accomplish tasks such as file manipulation, system monitoring, and more.
- **Command Suggestions**: Automatically provides the best command to achieve a goal based on user input.
- **Explanations**: Understand how each command works with detailed explanations, enhancing learning and usability.
- **Context Awareness**: OpenCMD keeps track of previous commands and adapts suggestions accordingly.

## Installation

To install OpenCMD, follow these steps:

1. Clone this repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the directory:
    ```bash
    cd OpenCMD
    ```
3. Install the required dependencies and package:
    ```bash
    pip install .
    ```

## How to Use

1.	After installation, launch OpenCMD by typing the following in your terminal:
    ```bash
    opencmd
    ```
2.	Interact with the tool using natural language commands. For example:
    ```bash
    % opencmd
    > Create a folder
    ```
3. 	OpenCMD will suggest the most appropriate command:
    ```bash
    mkdir <folder_name>
    exit
    ```
    You can navigate the options using the arrow keys, and an explanation will be displayed at the bottom of the screen.

4. If specific input is required, OpenCMD will prompt you for the necessary value:
    ```bash
    Please provide the value for 'folder_name': my_folder
    ```

5. For operations that modify the system (e.g., creating, deleting, or modifying files/folders, or changing a password), you will receive a confirmation prompt:
    ```bash
    Do you want to execute the command: mkdir my_folder? (y/n):
    ```

## Requirement

You need to configure the LLM API key in the OpenCMD environment to use this tool.


## Troubleshooting

- Command not recognized: Ensure that all system dependencies are installed correctly.
- Model not responding: Check your API key configuration for the LLM and verify network connectivity.

For additional help, feel free to raise an issue in the GitHub repository.

## Contribution

We welcome contributions! Please submit a pull request or open an issue to discuss any features, bug fixes, or improvements.