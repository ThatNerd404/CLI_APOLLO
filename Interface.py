from da_console import console
from LLAMA_Worker import Llama_Worker
import os
import sys
import time
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
    def run(self):
        console.print("Input your prompt then press enter. Type /quit to leave.")
        while True:
               query = input("\nUser: ")
               if query == "/quit":
                      console.print("bye bye!",style="green")
                      sys.exit(1)
               else:
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