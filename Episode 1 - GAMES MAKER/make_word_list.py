def make_local_list():
    allowed_word = []
    with open("/usr/share/dict/words") as f:
        for line in f:
            word = line.strip()
            if len(word) == 5 and not word[0].isupper():
                allowed_word.append(word)
    
    with open("words5.txt", "w") as output:
        output.writelines("\n".join(allowed_word))

make_local_list()

def sort_answers():
    answers = []
    with open("answer_words.txt") as f:
        for line in f:
            word = line.strip()
            answers.append(word)

    answers.sort()
    with open("SAFE_answers.txt", "w") as output:
        output.writelines("\n".join(answers))

sort_answers()