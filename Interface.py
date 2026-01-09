from LLAMA_Worker import Llama_Worker
from MYSQL_DB_Worker import MySql_Worker
from custom_exceptions import (
    OllamaConnectionError, 
    OllamaTimeoutError, 
    OllamaHTTPError, 
    OllamaNetworkError,
    OllamaModelNotFoundError
)

from logging.handlers import RotatingFileHandler
from pathlib import Path
import os
import logging
import sys
import re
import time
import json

# TODO: add command to save a conversation with /sc to mysql database and then ask if they want a copy to the a json file
# TODO: add command to load a conversation file with /lc from mysql database or from a json file

class Main_Interface():
    def __init__(self,args,console):
                self.args = args
                self.console = console
                self.convo_history = [{"role":"system", "content":"You go by the name Apollo and you are a friendly helpful ai."}]
                self.Llama = None
                self.MySQL = None
                self.logger = None
                os.system("clear")

                script_dir = os.path.dirname(os.path.abspath(__file__))
                log_file = os.path.join(script_dir, 'Logs/log.log')
                if not os.path.exists(log_file):
                    open(log_file, "w").close()

                try:
                    self.logger = logging.getLogger("logger")
                    self.logger.setLevel(logging.DEBUG)
                    handler = RotatingFileHandler(
                    log_file, maxBytes=100000, backupCount=5, encoding="utf-8")
                    formatter = logging.Formatter(
                    '%(asctime)s - %(levelname)s - %(message)s',"%Y-%m-%d %H:%M:%S")
                    handler.setFormatter(formatter)
                    self.logger.addHandler(handler)
                    self.logger.debug("Finished Initialization")
                    self.logger.debug(f"Args: {self.args}")

                except Exception as e:
                    self.console.print(f"Warning: Failed to initialize logger: {e}", 
                             style="yellow bold")
                    self.logger = logging.getLogger("logger")
                    self.logger.addHandler(logging.NullHandler())

                try:
                    with self.console.status("Pre-loading model...", spinner="dots") as status:
                        self.Llama = Llama_Worker()
                        self.Llama.preload_model()

                except KeyboardInterrupt:
                    self.console.print("Keyboard interrupt detected, exiting application.")
                    sys.exit(0)

                except EOFError:
                    self.console.print("\nEOF detected. Exiting...")
                    self.logger.info("EOF detected, exiting application")
                    sys.exit(0)

                except OllamaHTTPError as e:
                    self.console.print(f"Error: HTTP {e.status_code} - {e.message}", style="red bold")
                    sys.exit(1)

                except OllamaConnectionError as e:
                    self.console.print(f"Error: {e.message}", style="red bold")
                    sys.exit(1)

                except OllamaTimeoutError as e:
                    self.console.print(f"Error: {e.message}", style="red bold")
                    sys.exit(1)

                except OllamaNetworkError as e:
                    self.console.print(f"Error: {e.message}\nRestart Ollama server and try again.", style="red bold")
                    sys.exit(1)

                except OllamaModelNotFoundError as e:
                    self.console.print(f"Error: {e.message}")
                    sys.exit(1)

                except Exception as e:
                    self.console.print(f"Critical error occurred in initializing models: {e}", style="red bold")
                    sys.exit(1)


    def run(self):
        """Main Loop"""
        self.console.print("""

          /$$$$$$  /$$$$$$$   /$$$$$$  /$$       /$$        /$$$$$$ 
         /$$__  $$| $$__  $$ /$$__  $$| $$      | $$       /$$__  $$
        | $$  \ $$| $$  \ $$| $$  \ $$| $$      | $$      | $$  \ $$
        | $$$$$$$$| $$$$$$$/| $$  | $$| $$      | $$      | $$  | $$
        | $$__  $$| $$____/ | $$  | $$| $$      | $$      | $$  | $$
        | $$  | $$| $$      | $$  | $$| $$      | $$      | $$  | $$
        | $$  | $$| $$      |  $$$$$$/| $$$$$$$$| $$$$$$$$|  $$$$$$/
        |__/  |__/|__/       \______/ |________/|________/ \______/ 
                                                                    
                                                                    
        """, justify="center", style="#fcc200")
        self.console.rule("", style="#fcc200")
        self.console.print("Type /h for assistance!")

        while True:
             self.console.print("\nUser: ", style="bold #00643e",end="")
             try:
                self.query = input("")

             except EOFError:
                self.console.print("\nEOF detected. Exiting...", style="yellow")
                self.logger.info("EOF detected, exiting application")
                sys.exit(0)

             except KeyboardInterrupt:
                self.console.print("\n\nKeyboard interrupt detected. Exiting...", style="yellow")
                self.logger.info("Keyboard interrupt during input")
                sys.exit(0)

             if not self.query or not self.query.strip():
                continue

             elif self.query == "/q":
                self.quit_command()

             elif self.query == "/r":
                self.reset_command()

             elif "/lf" in self.query:
                self.load_file_command()

             elif "/pm" in self.query:
                self.pull_model_command()

             elif "/sm" in self.query:
                self.swap_model_command()

             elif self.query == "/lm":
                self.list_model_command()

             elif self.query == "/sc":
                self.save_conversation_command()

             elif self.query == "/lc":
                self.load_conversation_command()

             elif self.query == "/h":
                self.help_command()

             else:
                self.generate_response_command()

    def quit_command(self):
        self.logger.info("quit command has been used")
        while True:
            self.console.print("Are you sure you would like to quit? Your conversation will not be saved!\nY or N?", justify="center",style="bold red")
            self.console.print("\nUser: ", style="bold #00643e",end="")
            try:
                confirm = input("")
                if confirm.upper() == "Y":
                    self.logger.info("quitting application")
                    sys.exit(0)
                elif confirm.upper() == "N":
                    break

                else:
                    self.console.print("\nInvalid Input! Try Y or N!")

            except EOFError:
                self.console.print("\nEOF detected. Exiting...", style="yellow")
                self.logger.info("EOF detected, exiting application")
                sys.exit(0)

            except KeyboardInterrupt:
                self.console.print("\n\nKeyboard interrupt detected. Exiting...", style="yellow")
                self.logger.info("Keyboard interrupt during input")
                sys.exit(0)


    def reset_command(self):
        self.logger.info("reset command was used")
        self.convo_history = [{"role":"system", "content":"You go by the name Apollo and you are a friendly helpful ai."}]
        os.system('clear')
        self.run()

    def load_file_command(self):
        self.logger.info("load command was used")
        match = re.search(r"/lf\s+([^\s]+)", self.query)

        if not match:
            self.console.print("Usage: /lf filename.", style="yellow bold")
            return

        filename = match.group(1).strip()
        home_dir = Path.home()
        try:
            file_path = None
            with self.console.status("Locating File...", spinner="dots") as status:
                for root, dirs, files in os.walk(home_dir):
                    if filename in files:
                        file_path = os.path.join(root, filename)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_contents = f.read()
            status.stop()
        except FileNotFoundError:
            status.stop()
            self.console.print(f"Error: Failed to locate file: {filename}", style="red bold")
            return

        except PermissionError:
            status.stop()
            self.console.print(f"Error: No permission to read file: {filename}",style = "red bold")
            return

        except Exception as e:
            status.stop()
            self.console.print(f"Unexpected error occured: {e}", style="red bold")
            return

        if not file_path:
            self.console.print("File not found", style = "red bold")
            return

        self.console.print(f"Apollo: ", style= "yellow", end="")

        self.console.print(f"File loaded: {filename}", style="green bold")
        self.logger.info(f"Found file at: {file_path}")
        self.convo_history.append({"role": "system", "content":f"Use this document contents to inform your response: {file_contents}"})
        self.logger.info(f"file loaded: {filename}")

    def pull_model_command(self):
        self.logger.info("pull model command used")
        match = re.search(r"/pm\s+([^\s]+)", self.query)
        if not match:
            self.console.print("Usage: /pm model_name.", style="yellow bold")
            return
        model_name = match.group(1).strip()

        try:
            with self.console.status("Pulling model...", spinner="dots") as status:
                downloaded_model = self.Llama.pull_model(model_name)
            status.stop()
            self.console.print(f"Apollo: {downloaded_model} downloaded successfully!")

        except KeyboardInterrupt:
            self.console.print("Canceled", style="red bold")
            return

        except EOFError:
            self.console.print("Canceled", style="red bold")
            return

        except OllamaHTTPError as e:
            self.console.print(f"Error: HTTP {e.status_code} - {e.message}", style="red bold")
            return

        except OllamaConnectionError as e:
            self.console.print(f"Error: {e.message}", style="red bold")
            return

        except OllamaTimeoutError as e:
            self.console.print(f"Error: {e.message}", style="red bold")
            return

        except OllamaNetworkError as e:
            self.console.print(f"Error: {e.message}\nRestart Ollama server and try again.", style="red bold")
            return

        except OllamaModelNotFoundError as e:
            self.console.print(f"Error: {e.message}")
            return

        except Exception as e:
            self.console.print(f"Unexpected error occurred: {e}", style="red bold")
            return

        if not downloaded_model:
            return

        self.logger.info(f"Downloaded model: {downloaded_model}")

    def swap_model_command(self):
        self.logger.info("swap model command used")
        match = re.search(r"/sm\s+([^\s]+)", self.query)
        if not match:
            self.console.print("Usage: /sm model_name.", style="yellow bold")
            return

        model_name = match.group(1).strip()
        try:
            with self.console.status("Swapping model...", spinner="dots") as status:
                swapped_model = self.Llama.swap_model(model_name)
            status.stop()
            self.console.print(f"Swapped to model: {swapped_model}")

        except KeyboardInterrupt:
            self.console.print("Canceled", style="red bold")
            return

        except EOFError:
            self.console.print("Canceled", style="red bold")
            return

        except OllamaHTTPError as e:
            self.console.print(f"Error: HTTP {e.status_code} - {e.message}", style="red bold")
            return

        except OllamaConnectionError as e:
            self.console.print(f"Error: {e.message}", style="red bold")
            return

        except OllamaTimeoutError as e:
            self.console.print(f"Error: {e.message}", style="red bold")
            return

        except OllamaNetworkError as e:
            self.console.print(f"Error: {e.message}\nRestart Ollama server and try again.", style="red bold")
            return

        except OllamaModelNotFoundError as e:
            self.console.print(f"Error: {e.message}")
            return

        except Exception as e:
            self.console.print(f"Unexpected error occurred: {e}", style="red bold")
            return

        if not swapped_model:
            return
        self.logger.info(f"Swapped Model: {swapped_model}")

    def list_model_command(self):
        self.logger.info("list model command used")

        try:
            with self.console.status("Listing models...", spinner="dots") as status:
                running_model, stored_models = self.Llama.list_model()
            self.console.print(f"Apollo:",style="yellow bold")
            self.console.print(f"Currently running model: {running_model}")
            self.console.print("Installed models:")
            self.console.print("\n".join(stored_models))

        except KeyboardInterrupt:
            self.console.print("Canceled", style="red bold")
            return

        except EOFError:
            self.console.print("Canceled", style="red bold")
            return

        except OllamaHTTPError as e:
            self.console.print(f"Error: HTTP {e.status_code} - {e.message}", style="red bold")
            return

        except OllamaConnectionError as e:
            self.console.print(f"Error: {e.message}", style="red bold")
            return

        except OllamaTimeoutError as e:
            self.console.print(f"Error: {e.message}", style="red bold")
            return

        except OllamaNetworkError as e:
            self.console.print(f"Error: {e.message}\nRestart Ollama server and try again.", style="red bold")
            return

        except OllamaModelNotFoundError as e:
            self.console.print(f"Error: {e.message}")
            return

        except Exception as e:
            self.console.print(f"Unexpected error occurred: {e}", style="red bold")
            return

        if not running_model or not stored_models:
            return

        self.logger.info(f"Currently running model: {running_model}")
        self.logger.info(f"Loaded Models: {stored_models}")

    def save_conversation_command(self):
        # this command will have to turn the convo history dict into json object then store that object in a table
        self.logger.info("save conversation command was used")

        try:
            with self.console.status("Saving Conversation...", spinner="dots") as status:
                MySQL = MySql_Worker(host="100.111.62.92", user="root", password = "Secret_PW", port =8000, database="Conversation_Storage")
                running_model, stored_models = self.Llama.list_model()
                MySQL.Insert_Conversation(self.convo_history, running_model)

            self.console.print("Successfully saved conversation to database.", style="green bold")

        except Exception as e:
            self.console.print(f"Critical error occurred in connecting to database")
            return

    def load_conversation_command(self):
        pass

    def help_command(self):
        self.logger.info("help command was used")
        self.console.rule("HELP", style="#fcc200 bold")
        self.console.print("""
/h: Brings up this dialog.
/q: Asks for confirmation, then quits the application.
/r: Resets the conversation history and clears the screen.
/lf filename: starts on the home directory, searches for a file and loads a file into the conversation history.
/pm model_name: pulls a model from the ollama directory and downloads it.
/sm model_name: swaps current model into different one.
/lm: lists the current running model aka model currently in memory and then lists the models installed.
/sc: saves a conversation to the mysql database and ask if a copy should also be saved to a txt file.
/lc: loads a conversation from either the mysql database or from a txt file.
""", style = "blue")

        self.console.rule("", style="#fcc200 bold")

    def generate_response_command(self):
        self.logger.info("generate response command used")
        self.convo_history.append({"role":"user","content": self.query})
        start_time = time.perf_counter()
        response = ""
        response_started = False
        try:
            with self.console.status("Generating Response...", spinner="dots") as status:
                for chunk in self.Llama.generate_response(self.convo_history):
                    if not response_started:
                        status.stop()
                        self.console.print("Apollo: ",style="#fcc200",end="")
                        response_started = True

                    self.console.print(chunk, end="")
                    response += chunk

        except KeyboardInterrupt:
            self.console.print("Canceled", style="red bold")
            return

        except EOFError:
            self.console.print("Canceled", style="red bold")
            return

        except OllamaHTTPError as e:
            self.console.print(f"Error: HTTP {e.status_code} - {e.message}", style="red bold")
            return

        except OllamaConnectionError as e:
            self.console.print(f"Error: {e.message}", style="red bold")
            return

        except OllamaTimeoutError as e:
            self.console.print(f"Error: {e.message}", style="red bold")
            return

        except OllamaNetworkError as e:
            self.console.print(f"Error: {e.message}\nRestart Ollama server and try again.", style="red bold")
            return

        except OllamaModelNotFoundError as e:
            self.console.print(f"Error: {e.message}")
            return

        except Exception as e:
            self.console.print(f"Unexpected error occurred: {e}", style="red bold")
            return

        if not response:
            return

        self.convo_history.append({"role":"assistant","content": response})
        elapsed_time = time.perf_counter() - start_time
        self.logger.info(f"Response completed in {elapsed_time:.2f} seconds")


