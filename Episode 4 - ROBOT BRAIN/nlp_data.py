import csv
from collections import defaultdict
from scipy import spatial

def read_vectors(filename):
    data = {}

    topline = True 
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if topline:
                topline = False
            else:
                row_data = [float(i) for i in row[1:]]
                #any of the items are not 0, means that it's not an unknown word
                if any([i != 0 for i in row_data]):
                    data[row[0]] = row_data
    return data

def get_similarities_2_lists(data1, data2):
    """
    Gives back a dict where each word has a list of similarities with every other word
    """
    similarities  = defaultdict(list)
    for word1, vec1 in data1.items():
        for word2, vec2 in data2.items():
            sim = 1 - spatial.distance.cosine(vec1, vec2)
            similarities[word1].append(sim)
    return similarities

def max_closest(similarities):
    """
    Give each word a score that is the average of the 10 most similar things
    Default dict, so any words looked up in it that are unknown will be 0 (not similar at all)
    """
    max_scores = defaultdict(int)
    for word, sims in similarities.items():
        max_scores[word] = max(sims)
    return max_scores

def get_scores():
    data1 = read_vectors('wordle-words-output.csv')
    data2 = read_vectors('simpsons-output.csv')
    sims = get_similarities_2_lists(data1, data2)
    scores = max_closest(sims)
    return scores

def save_scores(scores, filename):
    with open(filename, "w") as f:
        writer = csv.writer(f)
        for k, v in scores.items():
            writer.writerow([k, v])

def load_scores(filename):
    scores = defaultdict(int)
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            word, score = row
            scores[word] = float(score)
    return scores   

if __name__ == "__main__":
    scores = get_scores()
    save_scores(scores, "scores_simpsonsmax.csv")