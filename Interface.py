from da_console import console
from LLAMA_Worker import Llama_Worker
from logging.handlers import RotatingFileHandler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import deque
import os
import logging
import sys 

#TODO add new command to load files into apollo with the /load filename.file maybe use the find command somehow?
#TODO add flag in command to specify which model to use 
#TODO add command to save a response with /save 
#TODO add a command to set timers to help with productivity and stuff
#TODO add a flag for doing a voice chat mode 


class Main_Interface():
    def __init__(self,args):
                self.args = args
                with open("/home/smartfella/programming_junk/CLI_APOLLO/sys_prompt.txt","r") as sys_instruct:
                    self.sys_prompt = sys_instruct.read()
                # makes the max length for the convo history 10 should add flag to change 
                self.convo_history = deque(maxlen=10)
                self.convo_history.append({"role": "system", "content": self.sys_prompt})
                
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
        console.print("Input your prompt then press enter. Type /quit to leave.")
        
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
                        self.convo_history = [{"role": "system", "content": self.sys_prompt}]
                        self.run()
                     elif query == "/load":
                        self.logger.info("load command was used")
                        e = os.path.realpath(os.system(f"find / -name {filename}")

                     elif query == "/help":
                        self.logger.info("help command was used")
                        console.rule("HELP", style="#fcc200 bold")
                        console.print("""
/help: brings up this dialog.
/quit: quits the application.
/reset: resets the conversation history.
/load {filename}: loads a file into the conversation history.
""", style="blue")
                                   
                     else:
                            self.logger.info("Response generation has begun")
                            self.convo_history.append({"role":"user","content": query})
                            Llama = Llama_Worker(model_path="/home/smartfella/programming_junk/CLI_APOLLO/Models/capybarahermes-2.5-mistral-7b.Q2_K.gguf",
                                                 messages=self.convo_history,
                                                 threads=8,
                                                 context=2048,
                                                 gpu_layers=0
                                                 )
                            with console.status("Generating Response...", spinner="dots") as status:
                                   response = Llama.generate_response(status)
                            self.convo_history.append({"role":"assistant","content": response})

               except Exception as e:
                      self.logger.error(f"Error Occurred: {e}")
                      console.print(f"Apollo has run into an unexpected error: {e}",style="red bold")
