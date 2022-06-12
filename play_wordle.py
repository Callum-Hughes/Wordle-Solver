from solver_functions import play_wordle

KNOWN_ANSWER = 'aloft'
answer, guesses = play_wordle(KNOWN_ANSWER, True, guesses=['raise'], method='props')

print(f'The answer is: {answer}.\nFound in {guesses} attempts.')
