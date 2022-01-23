from solver_functions import play_wordle
KNOWN_ANSWER = 'wince'
answer, guesses = play_wordle(KNOWN_ANSWER)

print(f'The answer is: {answer}.\nFound in {guesses} attempts.')
