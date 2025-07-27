from LLAMA_Worker import Llama_Worker
from Interface import Main_Interface
import sys


def main():
    if len(sys.argv) > 1:
        print("Usage: Type questions then press enter.\nType /quit to leave.")
    else:
        main_interface = Main_Interface()
        main_interface.run()

if __name__ == "__main__":
    main()
