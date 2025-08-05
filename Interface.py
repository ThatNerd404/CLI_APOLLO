from da_console import console
from LLAMA_Worker import Llama_Worker
from logging.handlers import RotatingFileHandler
import os
import logging
import sys 

class Main_Interface():
    def __init__(self):
                os.system('clear')
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
                self.convo_history = [{"role": "system", "content": "You are a helpful AI assisant named APOLLO. You refer to the user as Sir Cotterman.\n                          "}]
                
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
        console.print("Input your prompt then press enter. Type /quit to leave.")
        while True:
               try:
                     query = input("\nUser: ")
                     if query == "/quit":
                            self.logger.info("quit command has been used")
                            
                            while True:
                                confirm = input("\nAre you sure you would like to quit? Y or N?\nUser: ")
                                if confirm.upper() == "Y":
                                   console.print("Bye Bye!")
                                   sys.exit(1)
                                elif confirm.upper() == "N":
                                   break
                                
                                else:
                                   console.print("\nInvalid Input! Try Y or N!")
                               
                     elif query == "/help":
                    console.rule("HELP", style="#fcc200")
                     
                     elif query == "/reset":
                           self.logger.info("reset command has been used")
                           self.convo_history = [{"role": "system", "content": "You are a helpful AI assisant named APOLLO. You refer to the user as Sir Cotterman.\n                          "}]
                           console.print("Conversation history reset.", style="green bold")
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
