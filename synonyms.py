'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 20, 2023.
'''

import math
import re

def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    def dot_product(vec1, vec2):
        common_keys = set(vec1.keys()) & set(vec2.keys())
        return sum(vec1[key] * vec2[key] for key in common_keys)

    def magnitude(vec):
        return math.sqrt(sum(value ** 2 for value in vec.values()))

    dot_prod = dot_product(vec1, vec2)
    mag1 = magnitude(vec1)
    mag2 = magnitude(vec2)

    if mag1 == 0 or mag2 == 0:
        return 0.0

    similarity_fn = dot_prod / (mag1 * mag2)

    return similarity_fn
    pass


def build_semantic_descriptors(sentences):
    semantic_descriptors = {} # main dictionary

    for sentence in sentences: # iterate through all sentences

        for w, word in enumerate(sentence): # iterate through each word along with its
                                     # int value

            if word not in semantic_descriptors: # check for repetitive words in dict
                semantic_descriptors[word] = {}

            for c, check_word in enumerate(sentence): # check for other words in the
                                               # same sentence

                if w != c:
                    semantic_descriptors[word][check_word] = semantic_descriptors[word].get(check_word, 0) + 1
    return semantic_descriptors
    pass


def build_semantic_descriptors_from_files(filenames):
    semantic_descriptors = {}  # main dictionary

    for filename in filenames:
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()

            # Split text into sentences using ".", "!", "?" as sentence separators
            sentences = [sentence.strip() for sentence in re.split(r"[.!?]", text) if sentence.strip()]

            for sentence in sentences:
                # Split sentence into words using ",", "-", "--", ":", ";" as word separators
                words = [word.lower() for word in re.split(r"[, \-:;]+", sentence) if word]

                for w, word in enumerate(words):
                    if word not in semantic_descriptors:
                        semantic_descriptors[word] = {}

                    for c, check_word in enumerate(words):
                        if w != c:
                            semantic_descriptors[word][check_word] = semantic_descriptors[word].get(check_word, 0) + 1

    return semantic_descriptors


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):

    def get_similarity(word1, word2):

        if word1 in semantic_descriptors and word2 in semantic_descriptors:
            vector1 = semantic_descriptors[word1]
            vector2 = semantic_descriptors[word2]
            return similarity_fn(vector1, vector2)
        else:
            return -1

    max_similarity = -1
    most_similar_choice = choices[0]

    for choice in choices:
        similarity = get_similarity(word, choice)
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_choice = choice
        elif similarity == max_similarity and choices.index(choice) < choices.index(most_similar_choice):
            most_similar_choice = choice

    return most_similar_choice

def run_similarity_test(filename, semantic_descriptors, similarity_fn):

    correct_guesses = 0
    total = 0

    file = open(filename, "r")

    lines = file.readlines()

    for line in lines:

        words = line.split()

        if len(words) >= 3:

            word = words[0]
            correct_ans = words[1]
            choices = words[2:len(words)]

            choices = [choice.strip() for choice in choices]

            guess_ans = most_similar_word(word, choices, semantic_descriptors, cosine_similarity) # similarity_score acts as a placeholder for the tuple returned in most_similar_word

            if guess_ans == correct_ans:
                correct_guesses += 1

            total += 1

    if total == 0:
        return 0

    percent = correct_guesses * 100 / total

    return percent
    pass

if __name__ == '__main__':
    # sentences = [["i", "am", "a", "sick", "man"],
    #             ["i", "am", "a", "spiteful", "man"],
    #             ["i", "am", "an", "unattractive", "man"],
    #             ["i", "believe", "my", "liver", "is", "diseased"],
    #             ["however", "i", "know", "nothing", "at", "all", "about", "my",
    #             "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]
    # word = "i"
    # choices = ["am", "a", "man"]
    # semantic_descriptors = build_semantic_descriptors(sentences)
    # print(most_similar_word(word, choices, semantic_descriptors, cosine_similarity))
    sem_descriptors = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
    res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
    print(res, "of the guesses were correct")
