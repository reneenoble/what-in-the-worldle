from collections import defaultdict
import random
import os
from string import ascii_lowercase

def get_all_words():
    """
    Getting all the allowed guesses
    """
    

def get_total_count(words):
    """
    How many words does each letter appear in?
    """
    pass

def get_position_count(words):
    """
    How many times does a letter appear in each position?
    """
    pass


def colour_result(guess, answer):
    """
    Make the green, yellow and black hearts that match the guess
    """
    pass

def clear_screen():
    """
    blank screen so it looks like it's updating
    """
    pass




ALL_WORDS = get_all_words()
TOTAL_COUNT = get_total_count(ALL_WORDS)
POSITION_COUNT = get_position_count(ALL_WORDS)

# SEED = 1
# random.seed(SEED)

GREEN = "💚"
YELLOW = "💛"
BLACK = "🖤"



class Game():
    def __init__(self):
        pass

    def generate_answer(self):
        pass

    def play(self, solver):
        pass



class Solver():
    def __init__(self):
        pass

    def guess(self, guesses, results):
        pass

    def eliminate_words(self):
        pass

    def update_guess_info(self, guess, results):
        pass
    
    def _fixed_letters_correct(self, word):
        pass

    def _no_misplaced_repeating(self, word):
        pass


    def _letter_counts_in_range(self, word):
        pass


    def score_possibilites(self, allow_repeat_letters=False):
        pass





game = Game()
solver = Solver()
game.play(solver)


