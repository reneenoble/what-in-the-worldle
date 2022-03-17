from collections import defaultdict
import random
import os
from string import ascii_lowercase

def get_all_words():
    """
    Getting all the allowed guesses
    """
    with open("allowed_words.txt") as f:
    # with open("test_words.txt") as f:
        all_words = f.read().split("\n")
    return all_words
    

def get_total_count(words):
    """
    How many words does each letter appear in?
    """
    total_count = defaultdict(int)
    for word in words:
        for letter in word:
            total_count[letter] += 1
    return total_count

def get_position_count(words):
    """
    How many times does a letter appear in each position?
    """
    position_count = defaultdict(int)
    for word in words:
        for i, letter in enumerate(word):
            position_count[(i,letter)] += 1
    return position_count


def colour_result(guess, answer):
    """
    Make the green, yellow and black hearts that match the guess
    """
    output = [None for i in range(5)]

    answer_remaining = list(answer)
    for i in range(5):
        guess_letter = guess[i]
        answer_letter = answer[i]

        # colour in the greens
        if guess_letter == answer_letter:
            output[i] = GREEN
            answer_remaining.remove(answer_letter)

    for i, guess_letter in enumerate(guess):
        if guess_letter in answer_remaining and output[i] == None:
            output[i] = YELLOW
            answer_remaining.remove(guess_letter)

    for i, colour in enumerate(output):
        if colour == None:
            output[i] = BLACK

    return "".join(output)

def clear_screen():
    """
    blank screen so it looks like it's updating
    """
    os.system('clear' if os.name == 'nt' else 'clear')
    # "cls" instead of clear on windows




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
        self.turns = [] # guesses
        self.results = [] # green/yellow/black
        self.allowed_words = ALL_WORDS
        self.generate_answer()

    def generate_answer(self):
        # with open("official_answers.txt") as f:
        #     answers = f.read().split("\n")
        # self.answer = random.choice(answers)
        self.answer = "squid"

    def play(self, solver):
        view = ""
        for i in range(6):
            # guess = input("Enter a word: ").lower()
            # while guess not in self.allowed_words:
            #     print("That's not in our word list")
            #     guess = input("Enter a word: ").lower()

            guess = solver.guess(self.turns, self.results)
            
            
            self.turns.append(guess)
            self.results.append(colour_result(guess, self.answer))

            view += " ".join(list(guess.upper())) + "\n"
            view += colour_result(guess, self.answer) + "\n"
            view += "\n"
            
            # clear_screen()
            print(view)

            if guess == self.answer:
                print("You did it! 🎉🎉🎉")
                break
        else:
            print("bad luck!")
            print(f"The answer was { self.answer.upper() }")



class Solver():
    def __init__(self):
        self.possible_words = ALL_WORDS
        self.fixed_letters = [None for i in range(5)]

        # Note positions things could be in - None is no info, False is yellow or black, True is green
        # {"a": [None, None, False, None, True], "b"....}
        self.letter_position_info = {letter: [None for i in range(5)] for letter in ascii_lowercase}
        
        # Things could be in 0 to 5 places, before we have info
        self.letter_min_max = {letter: [0, 5] for letter in ascii_lowercase}


    def guess(self, guesses, results):
        if len(guesses) == 0:
            return self.score_possibilites()[0][0]
        else:
            self.update_guess_info(guesses[-1], results[-1])
            self.eliminate_words()
            print("Number of posible words: ", len(self.possible_words))
            return self.score_possibilites(allow_repeat_letters=True)[0][0]


    def eliminate_words(self):
        new_possible = []
        for word in self.possible_words:
            if not self._fixed_letters_correct(word):
                continue
            if not self._no_misplaced_repeating(word):
                continue
            if not self._letter_counts_in_range(word):
                continue
            new_possible.append(word)
        self.possible_words = new_possible

    def update_guess_info(self, guess, results):
        # Non-hard mode case - you get a green of a letter, that you have previously got a green letter for
        # Update the fixed letters, and then max to match green positions
        for i, pair in enumerate(zip(guess, results)):
            letter, result = pair
            if result == GREEN:
                self.fixed_letters[i] = letter
        
        # lock in min max from fixed letters
        letters = set(self.fixed_letters)
        for letter in letters:
            if letter != None:
                self.letter_min_max[letter][0] = self.fixed_letters.count(letter)

        # Guess with repeated letter, can reveal the exact number required, or up the minimum
        count_letter_results = defaultdict(list)
        for i, result_pair in enumerate(zip(guess, results)):
            #{"a": "<3 <3 <3"}
            letter, result = result_pair
            count_letter_results[letter].append(result)

        for letter, group_results in count_letter_results.items():
            letter_required = group_results.count(GREEN) + group_results.count(YELLOW)
            if BLACK in group_results:
                self.letter_min_max[letter] = [letter_required, letter_required]
            else:
                self.letter_min_max[letter][0] = letter_required

        # Update position info
        for i, pair in enumerate(zip(guess, results)):
            letter, result = pair
            if result == GREEN:
                self.letter_position_info[letter][i] = True
            else:
                self.letter_position_info[letter][i] = False
    
    def _fixed_letters_correct(self, word):
        for i, letter in enumerate(word):
            # if there is a fixed letter, and this doens't match, skip this word
            if self.fixed_letters[i] != None and self.fixed_letters[i] != letter:
                return False
        return True

    def _no_misplaced_repeating(self, word):
        # don't try a letter in a place you already know is wrong
        for i, letter in enumerate(word):
            # if you've tried a letter there before and it's wrong for that spont
            if self.letter_position_info[letter][i] == False:
                return False
        return True

    def _letter_counts_in_range(self, word):
        # removes words with eliminated letters
        # ensures words have a repeated letter if that is known from guess
        # ensure a previously yellow letter is somewhere in a word
        {"a":[1,2]}
        for letter, minmax in self.letter_min_max.items():
            min_letter, max_letter = minmax
            count = word.count(letter)
            if count < min_letter or count > max_letter:
                return False
        return True


    def score_possibilites(self, allow_repeat_letters=False):
        score_count = defaultdict(int)
        # if total_words == None:
        total_words = len(self.possible_words)

        for word in self.possible_words:
            if not allow_repeat_letters and len(set(list(word))) < len(word):
                continue
            # for letter in ["y", "w", "l", "r", "m", "n", "ng"]:
            #     if letter in word:
            #         score_count[word] += 0.5
            # for  letter in "aeiou":
            #     if letter in word:
            #         score_count[word] += 0.5
            for letter in set(list(word)):
                score_count[word] += 1 * TOTAL_COUNT[letter]/total_words
            for i, letter in enumerate(word):
                position_score = POSITION_COUNT[(i, letter)]/total_words
                score_count[word] += 1 * position_score

        sorted_score_count = sorted(list(score_count.items()), key=lambda x:x[1], reverse=True)
        return sorted_score_count





game = Game()
solver = Solver()
game.play(solver)


