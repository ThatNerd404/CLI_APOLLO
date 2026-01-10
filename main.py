from Interface import Main_Interface
import sys
import argparse
from rich.console import Console
# nonsense comment2
def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    console = Console()
    main_interface = Main_Interface(args,console) 
    main_interface.run()

if __name__ == "__main__":
    main()
