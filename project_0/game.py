"""Guess the number game
Computer thinks of and guesses the number
"""

from collections.abc import Callable
from types import NoneType
import numpy as np
from enum import Enum


class Hint(Enum):
    YOU_WON = 1
    TRY_GREATER = 2
    TRY_SMALLER = 3


def smart_guess(low: int, high: int, the_game: Callable[[int], Hint]):
    """Guesses the number by trying a random number from a range which reduces based on the game hints

    Args:
        low (int): A lower bound of numbers range to guess in. guess including this number
        high (int): A higher bound of numbers range to guess in. guess not including this number
        the_game (Callable[[int], Hint]): A function that takes a guess and returns a hint: `Hint.YOU_WON`, `Hint.TRY_SMALLER`, `Hint.TRY_GREATER`
    """
    while True:
        the_guess = np.random.randint(low, high)

        hint = the_game(the_guess)
        if hint is Hint.YOU_WON:
            break

        # print(the_guess, hint)

        if hint is Hint.TRY_GREATER:
            low = the_guess
        else:
            high = the_guess


def random_guess(low: int, high: int, the_game: Callable[[int], Hint]):
    """Guesses the number by trying a random number each time

    Args:
        low (int): A lower bound of numbers range to guess in. guess including this number
        high (int): A higher bound of numbers range to guess in. guess not including this number
        the_game (Callable[[int], Hint]): A function that takes a guess and returns `Hint.YOU_WON` if the guess is correct.
    """
    while True:
        the_guess = np.random.randint(low, high)

        if the_game(the_guess) is Hint.YOU_WON:
            break


def score_game(number_guesser: Callable[[int, int, Callable[[int], Hint]], None]) -> int:
    """Tests 1000 times in how many attempts on average the algirithm guesses the number

    Args:
        number_guesser: A function which, takes args:
                        - low (int): lower bound of numbers range to guess in. guess including this number
                        - high (int): higher bound of numbers range to guess in. guess not including this number
                        - the_game (Callable[[int], Hint]): another function
                        makes guesses and calls the game with each guess,
                        uses the game's returned value: `Hint.YOU_WON`, `Hint.TRY_SMALLER`, `Hint.TRY_GREATER` - to decide on what to do next

    Returns:
        int: average number of attempts
    """

    count_ls = []

    # np.random.seed(1)  # fix seed for reproduciablity of results

    # range of numbers to guess
    low = 1
    high = 101

    random_array = np.random.randint(
        low, high, size=(1000))  # the thought of numbers

    for number in random_array:
        attempts_count = 0

        def the_game(the_guess):
            nonlocal attempts_count

            attempts_count += 1

            if the_guess < number:
                return Hint.TRY_GREATER
            if the_guess > number:
                return Hint.TRY_SMALLER
            return Hint.YOU_WON

        number_guesser(low, high, the_game)

        count_ls.append(attempts_count)

    score = int(np.mean(count_ls))

    print(f"Your algorithm guesses using an average of {score} attempts ")

    return score


if __name__ == "__main__":
    # RUN
    score_game(smart_guess)
