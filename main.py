from LLAMA_Worker import Llama_Worker
from da_console import console
from Interface import Main_Interface
import sys
import os


def main():
    if len(sys.argv) > 1:
        print("Usage: Type questions then press enter.\nType /bye to leave.")
    else:
        main_interface = Main_Interface()
        main_interface.run()

if __name__ == "__main__":
    main()
#  TODO: finish with the cosmetics
#  TODO: add llm functionality that is async
#  TODO: add error handling 
