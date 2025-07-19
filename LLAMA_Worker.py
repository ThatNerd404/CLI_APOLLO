from llama_cpp import Llama
from da_console import console
import rich
import sys
import os
class Llama_Worker():
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