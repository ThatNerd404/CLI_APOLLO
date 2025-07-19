from da_console import console
from LLAMA_Worker import Llama_Worker
import os
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

    def run(self):
        while True:
               query = input()
               if query == "\\bye":
                      console.print("bye bye!",style="green blink")
                      sys.exit(1)