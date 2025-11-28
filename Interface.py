from LLAMA_Worker import Llama_Worker
from logging.handlers import RotatingFileHandler
import os
import logging
import sys
import re
import subprocess
import time

# TODO: add command to save a response with /s 
# TODO: change /lf feature to take file and generate embeddings, then store said embeddings in the database.
# TODO: create new command to query the database or possibly a flag? maybe make it always query the database?
# TODO: add error handling for logs to not prevent program from working when logs don't work and pass logs to all workers

class Main_Interface():
    def __init__(self,args, console):
                self.args = args
                self.console = console
                self.convo_history = []
                self.Llama = None
                self.logger = None
                try:
                    # pre-loading the ai model  
                    with self.console.status("Pre-loading model...", spinner="dots") as status:
                        self.Llama = Llama_Worker(self.console)
                except KeyboardInterrupt:
                    self.console.print("Keyboard interrupt detected, exitting application.")
                    sys.exit(1)
                except Exception as e:
                    self.console.print(f"Critical error occurred in initializing models: {e}", style="red bold")
                    sys.exit(1)
                try:
                # setting up the logger
                    self.logger = logging.getLogger("logger")
                    self.logger.setLevel(logging.DEBUG)
                    handler = RotatingFileHandler(
                    "Logs/log.log", maxBytes=100000, backupCount=5, encoding="utf-8")
                    formatter = logging.Formatter(
                    '%(asctime)s - %(levelname)s - %(message)s',"%Y-%m-%d %H:%M:%S")
                    handler.setFormatter(formatter)
                    self.logger.addHandler(handler)
                    self.logger.debug("Finished Initialization")
                    self.logger.debug(f"Args: {self.args}")

                except Exception as e:
                    self.console.print(f"Warning: Failed to initialize logger: {e}", 
                             style="yellow bold")
                    # Create a basic logger that at least doesn't crash
                    self.logger = logging.getLogger("logger")
                    self.logger.addHandler(logging.NullHandler())

    def run(self):
        """asdfasdfas"""
        os.system('clear')
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
               try:
                     self.console.print("\nUser: ", style="bold #00643e",end="")
                     try:
                        self.query = input("")

                     except EOFError:
                        self.console.print("\nEOF detected. Exiting...", style="yellow")
                        self.logger.info("EOF detected, exiting application")
                        sys.exit(0)

                     except KeyboardInterrupt:
                        self.console.print("\n\nKeyboard interrupt detected.", style="yellow")
                        self.logger.info("Keyboard interrupt during input")
                        continue

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

                     elif self.query == "/h":
                        self.help_command()

                     else:
                        self.generate_response_command()

               except Exception as e:
                      self.logger.error(f"Error Occurred: {e}")
                      self.console.print(f"Apollo has run into an unexpected error: {e}",style="red bold")

    def quit_command(self):
        self.logger.info("quit command has been used")
        while True:
            self.console.print("Are you sure you would like to quit? Your conversation will not be saved!\nY or N?", justify="center",style="bold red")
            self.console.print("\nUser: ", style="bold #00643e",end="")
            confirm = input("")
            if confirm.upper() == "Y":
                sys.exit(1)
            elif confirm.upper() == "N":
                break

            else:
                console.print("\nInvalid Input! Try Y or N!")

    def reset_command(self):
        self.logger.info("reset command was used")
        self.convo_history = []
        self.run()

    def load_file_command(self):
        self.logger.info("load command was used")
        match = re.search(r"/lf\s+([^\s]+)", self.query)
        if match:
            filename = match.group(1)
            try:
                with self.console.status("Locating File...", spinner="dots") as status:
                    result = subprocess.run(
                    ["find", "/", "-name", filename],
                    capture_output=True,
                    text=True
                    )
                path = result.stdout.strip().split("\n")[0] if result.stdout.strip() else None
                if path:
                    self.console.print(f"File loaded: {path}", style="red bold")
                    self.logger.info(f"Found file at: {path}")
                    with open(path,"r") as loaded_file:
                        file_contents = loaded_file.read()
                    embeddings = self.Llama.generate_embeddings(file_contents)
                    self.logger.info(f"file loaded: {filename}")
                    self.logger.info(f"embeddings generated: {embeddings}")
                else:
                    self.console.print("File not found.", style="bold red")
            except Exception as e:
                self.console.print(f"Error while searching: {e}", style="bold red")
        else:
            self.console.print("Usage: /load filename", style="bold yellow")

    def pull_model_command(self):
        self.logger.info("pull model command used")
        match = re.search(r"/pm\s+([^\s]+)", self.query)
        if match:
            model_name = match.group(1)
            with self.console.status("Pulling model...", spinner="dots") as status:
                downloaded_model = self.Llama.pull_model(model_name,status)
            self.logger.info(f"Downloaded model: {downloaded_model}")

    def swap_model_command(self):
        self.logger.info("swap model command used")
        match = re.search(r"/sm\s+([^\s]+)", self.query)
        if match:
            model_name = match.group(1)
            with self.console.status("Swapping model...", spinner="dots") as status:
                swapped_model = self.Llama.swap_model(model_name,status)
            self.logger.info(f"Swapped Model: {swapped_model}")

    def list_model_command(self):
        self.logger.info("list model command used")
        with self.console.status("Listing running model...", spinner="dots") as status:
            running_model = self.Llama.list_model(status)
        self.console.print("Currently running model:")
        self.console.print(running_model)


    def help_command(self):
        self.logger.info("help command was used")
        self.console.rule("HELP", style="#fcc200 bold")
        self.console.print("""
/h: brings up this dialog.
/q: quits the application.
/r: resets the conversation history.
/lf filename: loads a file into the conversation history.
/pm model_name: pulls a model from the ollama directory and downloads it.
/sm model_name: swaps current model into different one.
/lm: lists the current running model.
""", style="blue")
        self.console.rule("", style="#fcc200 bold")

    def generate_response_command(self):
        self.logger.info("Response generation has begun")
        self.convo_history.append({"role":"user","content": self.query})
        start_time = time.perf_counter() 
        
        with self.console.status("Generating Response...", spinner="dots") as status:
               response = self.Llama.generate_response(self.convo_history,status)
        self.convo_history.append({"role":"assistant","content": response})
        elapsed_time = time.perf_counter() - start_time
        self.logger.info(f"Response completed in {elapsed_time:.2f} seconds")


