import os
import shlex
import curses
import readline
import subprocess

from openai import OpenAI
from textwrap import dedent
from pydantic import BaseModel


client = OpenAI(api_key=os.environ.get('OPENAPI_API_KEY'))
MODEL  = "gpt-4o-mini"

class CMDHelper(BaseModel):
  class Cmd(BaseModel):
    explanation: str
    placeholder: str
    cmd: str

  options: list[Cmd]
  supported: bool
  write_operation: bool

def get_command_suggestions(user_description):
  system_role_content = f"""
  You are an expert in the {os.uname().sysname} operating system, running version {os.uname().version} on a {os.uname().machine} machine. Your role is to provide commands and explanations to help the user accomplish system-related tasks.
  Guidelines:
	1.	Supported Commands: Provide commands for system management tasks (e.g., managing files, directories, processes, or system configurations).
	a. If a request cannot be achieved via the command line or is not related to system management, return a boolean flag indicating “not supported.”
	b. For example, requests like “tell me a joke” or “show me the weather” are not supported, but commands like “what time is it” are supported.
	2.	Write Operations: For operations that modify the system (e.g., creating, deleting, or modifying files/folders, or changing a password), include a boolean flag to confirm the action in your response.
	3.	Placeholders: If the command requires user-specific input (e.g., file names, folder paths), provide placeholders surrounded by < and >. In your response, include a list of placeholder names separated by | in the placeholder field.
	a. Example: If the user requests a command to create a folder but doesn’t specify a name, include a placeholder like <folder_name>, and the placeholder field would be folder_name.
	4.	Human-readable Format: For requests related to file or folder sizes, always provide the information in human-readable format (e.g., using -h for size outputs).
  """
  
  request = f"Suggest relevant command line commands with explanations regarding the request '{user_description}'."
  response = client.beta.chat.completions.parse(
    model=MODEL,
    messages=[
        {"role": "system", 
          "content": dedent(system_role_content)},
        {
            "role": "user",
            "content": request
        }
    ],
    response_format=CMDHelper,
  )
  return (response.choices[0].message)

def execute_command(command):
  """
  Execute a given shell command.
  """
  try:
    # Split the command into arguments for safety using shlex
    args = shlex.split(command)
    # Handle the 'cd' command separately
    if args[0] == "cd":
      if len(args) > 1:
        try:
          os.chdir(args[1])  # Change the directory
          print(f"Changed directory to {os.getcwd()}")
        except FileNotFoundError:
          print(f"No such directory: {args[1]}")
      else:
          # If 'cd' is called without arguments, change to the home directory
          os.chdir(os.path.expanduser("~"))
          print(f"Changed directory to {os.getcwd()}")
    else:
      # Execute other commands normally
      result = subprocess.run(args, capture_output=True, text=True)
      # Print the result but do not include an empty line after the result
      print(result.stdout, end="")
      if result.returncode != 0:
          print(f"Error: {result.stderr}", flush=True)
  
  except Exception as e:
      print(f"Failed to execute command: {e}")

def setup_readline_history():
    """
    Setup readline for command history, allowing navigation with arrow keys.
    """
    history_file = os.path.expanduser("~/.cmd_proxy_history")
    try:
      readline.read_history_file(history_file)
    except FileNotFoundError:
      # No previous history exists
      pass
    readline.set_history_length(1000)  # Set a limit for command history

def save_readline_history():
  """
  Save the readline command history to a file.
  """
  history_file = os.path.expanduser("~/.cmd_proxy_history")
  readline.write_history_file(history_file)

def display_menu(stdscr, cmds, placesholders, descriptions):
  # Turn off cursor blinking
  curses.curs_set(0)
  
  # Get screen height and width
  height, width = stdscr.getmaxyx()

  current_option = 0

  while True:
    stdscr.clear()

    # Loop through options and highlight the current one
    for idx, option in enumerate(cmds):
      x = width//2 - len(option)//2
      y = height//2 - len(cmds)//2 + idx
      if idx == current_option:
        stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(y, x, option)
        stdscr.attroff(curses.A_REVERSE)
      else:
        stdscr.addstr(y, x, option)

    # Display the description of the selected option
    description = descriptions[current_option]
    stdscr.addstr(height-2, 0, description)  # Display at the bottom of the screen

    # Refresh the screen
    stdscr.refresh()

    # Wait for user input
    key = stdscr.getch()

    # Navigate the options with up/down arrow keys
    if key == curses.KEY_UP and current_option > 0:
      current_option -= 1
    elif key == curses.KEY_DOWN and current_option < len(cmds) - 1:
      current_option += 1
    elif key == ord('\n'):
        return cmds[current_option], placesholders[current_option]

def command_line():
  """
  The main command line interface function.
  """
  setup_readline_history()
  while True:
    try:
      user_input = input(f"> ")
      if user_input.strip().lower() == "exit":
        print("Exiting...")
        break
      command_suggestion = get_command_suggestions(user_input).parsed
      # print(command_suggestion)

      if (command_suggestion.supported):
        # Iterate through the options and display them in a menu
        cmds = [option.cmd for option in command_suggestion.options] + ["exit"]
        placesholders = [option.placeholder for option in command_suggestion.options] + [""]
        explanations = [option.explanation for option in command_suggestion.options] + ["Exit the current interface"]
        final_cmd, final_placeholders = curses.wrapper(lambda stdscr: display_menu(stdscr, cmds, placesholders, explanations))

        # print(final_cmd)
        if final_cmd:
          if final_cmd == "exit":
            pass
          else:
            if (final_placeholders):
              # Parse the placeholders and ask the user for values
              placeholders = final_placeholders.split("|")
              for placeholder in placeholders:
                placeholder_value = input(f"Please provide the value for '{placeholder}': ")
                final_cmd = final_cmd.replace(f"<{placeholder}>", placeholder_value)
            if command_suggestion.write_operation:
              user_confirmation = input(f"Do you want to execute the command: {final_cmd}? (y/n): ")
              if user_confirmation.strip().lower() == "y":
                execute_command(final_cmd)
            else:
              print(f"Executing the command: {final_cmd}")
              execute_command(final_cmd)
      else:
        print("The request is not supported.")
    except KeyboardInterrupt:
      print("Exiting...")
      break
  # Save the command history when exiting
  save_readline_history()

if __name__ == "__main__":
  command_line()