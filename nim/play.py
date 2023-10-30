from nim import train, play
import sys
import ast

def main():
    # Check if there are exactly two command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py <number> <list>")
        return

    # Get the number from the first argument
    try:
        number = int(sys.argv[1])
    except ValueError:
        print("Error: The first argument must be a valid integer.")
        return

    # Get the list from the second argument and validate the format
    try:
        input_list = ast.literal_eval(sys.argv[2])
        if not isinstance(input_list, list):
            raise ValueError
    except (ValueError, SyntaxError):
        print("Error: The second argument must be a valid list in the format [1,2,3,4].")
        return
    ai = train(number)
    play(ai, 0, input_list)

if __name__ == "__main__":
    main()


