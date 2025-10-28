from da_console import console
from LLAMA_Worker import Llama_Worker
from logging.handlers import RotatingFileHandler
from collections import deque
import os
import logging
import sys
import re
import subprocess
import time

#TODO add command to create todo lists and stuff
#TODO add flag in command to specify which model to use 
#TODO add command to save a response with /save 
#TODO add a flag for doing a voice chat mode 


class Main_Interface():
    def __init__(self,args):
                self.args = args
                # makes the max length for the convo history 10 should add flag to change 
                self.convo_history = []                
                # Setup logger and rotating file handler
                self.logger = logging.getLogger("logger")
                self.logger.setLevel(logging.DEBUG)
                handler = RotatingFileHandler(
                "/home/smartfella/programming_junk/CLI_APOLLO/Logs/log.log", maxBytes=100000, backupCount=5, encoding="utf-8")
                formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',"%Y-%m-%d %H:%M:%S")
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)

                self.logger.debug("Finished Initialization")

    def run(self):
        os.system('clear')
                #console.print(self.args)
        console.print("""

          /$$$$$$  /$$$$$$$   /$$$$$$  /$$       /$$        /$$$$$$ 
         /$$__  $$| $$__  $$ /$$__  $$| $$      | $$       /$$__  $$
        | $$  \ $$| $$  \ $$| $$  \ $$| $$      | $$      | $$  \ $$
        | $$$$$$$$| $$$$$$$/| $$  | $$| $$      | $$      | $$  | $$
        | $$__  $$| $$____/ | $$  | $$| $$      | $$      | $$  | $$
        | $$  | $$| $$      | $$  | $$| $$      | $$      | $$  | $$
        | $$  | $$| $$      |  $$$$$$/| $$$$$$$$| $$$$$$$$|  $$$$$$/
        |__/  |__/|__/       \______/ |________/|________/ \______/ 
                                                                    
                                                                    
        """, justify="center", style="#fcc200")
        console.rule("", style="#fcc200")
        console.print("Type /help for assistance!")
        
        while True:
               try:
                     console.print("\nUser: ", style="bold #00643e",end="")
                     query = input("")
                     if query == "/quit":
                        self.logger.info("quit command has been used")

                        while True:
                            console.print("Are you sure you would like to quit? Your conversation will not be saved!\nY or N?", justify="center",style="bold red")
                            console.print("\nUser: ", style="bold #00643e",end="")
                            confirm = input("")
                            if confirm.upper() == "Y":
                                sys.exit(1)
                            elif confirm.upper() == "N":
                                break

                            else:
                                console.print("\nInvalid Input! Try Y or N!")
                     
                     elif query == "/reset":
                        self.logger.info("reset command was used")
                        self.convo_history = []
                        self.run()

                     elif "/load" in query:
                        self.logger.info("load command was used")
                        match = re.search(r"/load\s+([^\s]+)", query)
                        if match:
                            filename = match.group(1)
                            try:
                                with console.status("Locating File...", spinner="dots") as status:
                                    result = subprocess.run(
                                    ["find", "/", "-name", filename],
                                    capture_output=True,
                                    text=True
                                    )
                                path = result.stdout.strip().split("\n")[0] if result.stdout.strip() else None
                                if path:
                                    console.print(f"File loaded: {path}", style="red bold")
                                    self.logger.info(f"Found file at: {path}")
                                    with open(path,"r") as loaded_file:
                                        file_contents = loaded_file.read()
                                        self.convo_history.append({
                                            "role": "assistant",
                                            "content": f"(Reference document loaded from {filename}):\n\n{file_contents}"})
                                    self.logger.info(f"file loaded:{filename}")
                                else:
                                    console.print("File not found.", style="bold red")
                            except Exception as e:
                                console.print(f"Error while searching: {e}", style="bold red")
                        else:
                            console.print("Usage: /load filename", style="bold yellow")
                     elif query == "/todo":
                        self.logger.info("todo command was used")
                        console.rule("TODO", style="#fcc200 bold")
                        console.print("This is where my todo-list would be...\nIF I HAD ONE!!!")
                     elif query == "/help":
                        self.logger.info("help command was used")
                        console.rule("HELP", style="#fcc200 bold")
                        console.print("""
/help: brings up this dialog.
/quit: quits the application.
/reset: resets the conversation history.
/load {filename}: loads a file into the conversation history.
/todo: brings up the todo dialog where you create and use todo-lists.
""", style="blue")
                                   
                     else:
                            self.logger.info("Response generation has begun")
                            self.convo_history.append({"role":"user","content": query})
                            start_time = time.perf_counter() 
                            Llama = Llama_Worker(messages=self.convo_history
                                                 )
                            with console.status("Generating Response...", spinner="dots") as status:
                                   response = Llama.generate_response(status)
                            self.convo_history.append({"role":"assistant","content": response})
                            elapsed_time = time.perf_counter() - start_time
                            self.logger.info(f"Response completed in {elapsed_time:.2f} seconds")
               except Exception as e:
                      self.logger.error(f"Error Occurred: {e}")
                      console.print(f"Apollo has run into an unexpected error: {e}",style="red bold")
