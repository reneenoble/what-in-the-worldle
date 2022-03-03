GREEN = "💚"
YELLOW = "💛"
BLACK = "🖤"

import os 
def clear_screen():
    os.system('clear' if os.name == 'nt' else 'clear')
    # "cls" instead of clear on windows

def colour_result(guess, answer):
    """
    words should be lowercase
    words are the same length
    """

    word_len = len(guess)
    answers_letters_remaining = list(answer)

    # output = []
    # for i in range(word_len):
    #     output.append(None)    

    output = [None for i in range(word_len)]
    
    # Add in green letters
    for i in range(word_len):
        guess_letter = guess[i]
        answer_letter = answer[i]
        if guess_letter == answer_letter:
            output[i] = GREEN
            answers_letters_remaining.remove(guess_letter)

    # do the yellow colorus
    for i, guess_letter in enumerate(guess):
        if output[i] == None and guess_letter in answers_letters_remaining:
            output[i] = YELLOW
            answers_letters_remaining.remove(guess_letter)

    for i, colour in enumerate(output):
        if colour == None:
            output[i] = BLACK

    return " ".join(output)

# answer = "color"
# guess = "sores"
# print(colour_result(guess, answer))

import random
SEED = 1
random.seed(SEED)

# Get todays answer
with open("SAFE_answers.txt") as f:
    answers = f.read().split("\n")
answer = random.choice(answers)
print(answer)

# Get todays answer
with open("allowed_words.txt") as f:
    allowed_words = f.read().split("\n")

clear_screen()
view = ""
NUM = 6
for i in range(NUM):
    # guess entry
    guess = input("Enter a word: ").lower()
    while guess not in allowed_words:
        print("That's not in our word list")
        guess = input("Enter a word: ").lower()

    view += "  ".join(list(guess.upper())) + "\n"
    view += colour_result(guess, answer) + "\n\n"
    clear_screen()
    print(view)

    if guess == answer:
        print("You did it! 🎉🎉🎉")
        break
else:
    print("you lose!")
    print(f"The answer was { answer.upper() }.")