import math
import re

from typing import Callable, Optional, Tuple


def prompt_until_predicate_met(prompt: str, error: Callable[[str], Optional[str]]) -> str:
    """
    Prompts the user for input until the error function returns None and returns the user's input.
    :param prompt: The prompt to display to the user
    :param error: The function that takes the user's input and returns an error message if the input is invalid, or None
                  if the input is valid
    :return: The user's input
    """
    while True:
        user_input = input(prompt)
        error_message = error(user_input)
        if error_message is None:
            return user_input
        else:
            print(f"Error: {error_message}")


def get_user_range() -> Tuple[int, int]:
    """
    Prompts the user for input until the user enters a valid range and subsequently returns the range as a tuple.
    :return: The range of integers as a tuple
    """
    
    # Regex to match an integer
    int_regex = re.compile(r"^-?\d+$")
    
    # Validates that a number is an integer
    integer_validator = lambda n: "Please enter a valid integer." if int_regex.match(n) is None else None
    
    # Validates that the end of the range is greater than or equal to the start of the range
    end_greater_than_start_validator = lambda n: "The end of the range must be greater than " \
                                                 "or equal to the start of the range." if int(n) < start else None
    
    start = int(
        prompt_until_predicate_met(
            "Please enter the start of the range of integers you want to choose from: ",
            integer_validator
        )
    )
    print()
    
    end = int(
        prompt_until_predicate_met(
            "Please enter the end of the range of integers you want to choose from: ",
            lambda n: integer_validator(n) or end_greater_than_start_validator(n)
        )
    )
    print()
    
    return start, end


def binary_search_guess_number(start: int, end: int) -> Optional[Tuple[int, int]]:
    """
    Guesses the number the user is thinking of in a range of integers using binary search and returns the user's
    number and the number of guesses it took to guess the user's number if they did not cheat or None otherwise.
    :param start: The start of the range of integers
    :param end: The end of the range of integers
    :return: The tuple of the user's number and the number of guesses it took to guess the user's number if they did
             not cheat or None otherwise
    """
    num_guesses = 0
    
    while start <= end:
        num_guesses += 1
        # Note: I am aware of //, but I use this to ensure that the result rounds towards 0 instead of -inf
        mid = int((start + end) / 2)
        
        guess_comparison = prompt_until_predicate_met(
            f"Is your number {mid}? Enter 'h' if your number is higher, "
            "'l' if your number is lower, or 'c' if my guess is correct: ",
            lambda comparison: "Please enter 'h', 'l', or 'c'." if comparison not in {"h", "l", "c"} else None
        )
        
        if guess_comparison == "h":
            start = mid + 1
        elif guess_comparison == "l":
            end = mid - 1
        else:
            return mid, num_guesses
    return None


def main() -> None:
    """
    The runner function for the program.
    :return: None
    """
    print("I will attempt to guess a number you are thinking of in a range of integers.\n")
    
    start, end = get_user_range()
    
    num_tries = math.floor(math.log2(end - start + 1)) + 1
    print("Think of a number between the start and end of the range you entered.")
    print(
        f"I will guess the number you are thinking of in {num_tries} tries or less.\n"
    )
    
    result = binary_search_guess_number(start, end)
    print()
    
    if result is None:
        print("You are a dirty cheater, aren't you? You must not even have had a number in mind.")
    else:
        print(f"I guessed your number {result[0]} in {result[1]}/{num_tries} guesses!")


if __name__ == '__main__':
    main()
