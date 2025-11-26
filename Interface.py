from LLAMA_Worker import Llama_Worker
from logging.handlers import RotatingFileHandler
import os
import logging
import sys
import re
import subprocess
import time

# TODO: add command to save a response with /s 
# TODO: add markitdown for creating RAG

class Main_Interface():
    def __init__(self,args, console):
                self.args = args
                self.console = console
                self.convo_history = []

                # pre-loading the ai model  
                with self.console.status("Pre-loading model...", spinner="dots") as status:
                    self.Llama = Llama_Worker(self.console)

                # setting up the logger
                self.logger = logging.getLogger("logger")
                self.logger.setLevel(logging.DEBUG)
                handler = RotatingFileHandler(
                "/home/smartfella/programming_junk/CLI_APOLLO/Logs/log.log", maxBytes=100000, backupCount=5, encoding="utf-8")
                formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',"%Y-%m-%d %H:%M:%S")
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
                self.logger.debug("Finished Initialization")
                self.logger.debug(f"Args: {self.args}")

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
                     query = input("")
                     if query == "/q":
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
                     
                     elif query == "/r":
                        self.logger.info("reset command was used")
                        self.convo_history = []
                        self.run()

                     elif "/lf" in query:
                        self.logger.info("load command was used")
                        match = re.search(r"/l\s+([^\s]+)", query)
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
                                        self.convo_history.append({
                                            "role": "assistant",
                                            "content": f"(Reference document loaded from {filename}):\n\n{file_contents}"})
                                    self.logger.info(f"file loaded:{filename}")
                                else:
                                    self.console.print("File not found.", style="bold red")
                            except Exception as e:
                                self.console.print(f"Error while searching: {e}", style="bold red")
                        else:
                            self.console.print("Usage: /load filename", style="bold yellow")
                     
                     elif "/pm" in query:
                        self.logger.info("pull model command used")
                        match = re.search(r"/pm\s+([^\s]+)", query)
                        if match:
                            model_name = match.group(1)
                            with self.console.status("Pulling model...", spinner="dots") as status:
                                downloaded_model = self.Llama.pull_model(model_name,status)
                            self.logger.info(f"Downloaded model: {downloaded_model}")

                     elif "/sm" in query:
                        self.logger.info("swap model command used")
                        match = re.search(r"/sm\s+([^\s]+)", query)
                        if match:
                            model_name = match.group(1)
                            with self.console.status("Swapping model...", spinner="dots") as status:
                                swapped_model = self.Llama.swap_model(model_name,status)
                            self.logger.info(f"Swapped Model: {swapped_model}")
                     elif query == "/lm":
                        self.logger.info("list model command used")
                        with self.console.status("Listing running models...", spinner="dots") as status:
                            running_models = self.Llama.list_model(status)
                        self.console.print("Currently running models:")
                        for model in running_models:
                            self.console.print(model)
                     elif query == "/h":
                        self.logger.info("help command was used")
                        self.console.rule("HELP", style="#fcc200 bold")
                        self.console.print("""
/h: brings up this dialog.
/q: quits the application.
/r: resets the conversation history.
/lf filename: loads a file into the conversation history.
/pm model_name: pulls a model from the ollama directory and downloads it.
/sm model_name: swaps current model into different one.
/lm: lists the current running models.
""", style="blue")
                                   
                     else:
                            self.logger.info("Response generation has begun")
                            self.convo_history.append({"role":"user","content": query})
                            start_time = time.perf_counter() 
                            
                            with self.console.status("Generating Response...", spinner="dots") as status:
                                   response = self.Llama.generate_response(self.convo_history,status)
                            self.convo_history.append({"role":"assistant","content": response})
                            elapsed_time = time.perf_counter() - start_time
                            self.logger.info(f"Response completed in {elapsed_time:.2f} seconds")

               except Exception as e:
                      self.logger.error(f"Error Occurred: {e}")
                      self.console.print(f"Apollo has run into an unexpected error: {e}",style="red bold")
