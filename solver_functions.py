import pandas as pd
import string

def get_words():
    potential_words = []
    for l in string.ascii_uppercase:
        with open(f'.\Word lists in csv\{l}word.csv') as f:
            words = f.readlines()
            words = [w.strip(' \n') for w in words]
            words = list(set([w for w in words if len(w) == 5]))
        potential_words.extend(words)
    
    return potential_words

def get_letter_score_map():
    with open(f'scrabble_scores.csv') as f:
        letters = f.readlines()
        letters = [l.strip(' \n').split(',') for l in letters][1:]
    
    letter_score_map = {}
    for l in letters:
        letter_score_map[l[0]] = int(l[1])

    return letter_score_map

def scrabble_scorer(word, letter_score_map = get_letter_score_map()):
    score = 0
    for w in word:
        try:
            score += letter_score_map[w]
            count = word.count(w)
            if count > 1:
                score += 2
        except:
            score += 999
    return score

def generate_word_scores():
    words = get_words()
    letter_score_map = get_letter_score_map()
    scores = list(map(lambda x: scrabble_scorer(x, letter_score_map), words))
    words_scores = pd.DataFrame(data=scores, index=words, columns=['scores']).sort_values(by=['scores'])

    return words_scores

def checker(guess, answer):
    output = []
    idx = 0
    for l in guess:
        if answer[idx] == l:
            output.append((l, 2))
        elif l in answer:
            output.append((l, 1))
        else:
            output.append((l, 0))
        idx += 1
    return output

def words_filter(words_scores, checked_word):
    position = 5 - len(checked_word)
    if position == 0:
        word = ''.join([x[0] for x in checked_word])
        words_scores = words_scores[~(words_scores.index == word)]
    if position != 5:
        x, *xs = checked_word
        if x[1] == 0:
            words_scores = words_filter(words_scores.filter(regex=f'^((?!{x[0]}).)*$', axis=0), xs)
        elif x[1] == 1:
            words_scores = words_filter(words_scores.filter(regex=f'{x[0]}', axis=0), xs)
        else:
            words_scores = words_filter(words_scores.filter(regex=f'^.{{{position}}}{x[0]}.*', axis=0), xs)
    return words_scores

def wordle_scorer(checked_word):
    scores = [x[1] for x in checked_word]
    return sum(scores)

answer_emoji_map = {0: '\U0001F7E5', 1: '\U0001F7E8', 2: '\U0001F7E9'}

def pretty_answer(checked_word):
    output = [answer_emoji_map[x[1]] for x in checked_word]
    return ''.join(output)

def play_wordle(known_answer):
    words_scores = generate_word_scores()
    no_guesses = 0
    score = 0
    while score != 10 and len(words_scores) != 0:
        no_guesses += 1
        guessed_word = words_scores.index[0]
        checked = checker(guessed_word, known_answer)
        score = wordle_scorer(checked)
        words_scores = words_filter(words_scores, checked)
        print(guessed_word)
        print(pretty_answer(checked))
    return guessed_word, no_guesses