from Interface import Main_Interface
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main_interface = Main_Interface(args)
    main_interface.run()

if __name__ == "__main__":
    main()
