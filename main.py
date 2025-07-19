import sys
from LLAMA_Worker import Llama_Worker
def main():
    if len(sys.argv) > 1:
        print("Usage: Type questions then press enter.\nType /bye to leave.")
    else:
        llama = Llama_Worker()


if __name__ == "__main__":
    main()
#  TODO: finish with the cosmetics
#  TODO: add llm functionality that is async
#  TODO: add error handling 
