import argparse
import random
import sys
import urllib.request
import os

from cowsay import cowsay, list_cows

MY_COW = list_cows()[24]
def bullscows(guess: str, secret: str) -> (int, int):
    bulls = sum(g == s for g, s in zip(guess, secret))
    cows = sum(min(secret.count(g), guess.count(g)) for g in set(guess))
    cows -= bulls
    return bulls, cows

def gameplay(ask, inform, words: list[str]) -> int:
    secret_word = random.choice(words)
    attempts = 0
    while True:
        user_guess = ask("Type a word ", words)
        # print(f'guess = {user_guess}, word = {secret_word}')
        bulls, cows = bullscows(user_guess, secret_word)
        inform("Bulls: {}, Cows: {}", bulls, cows)
        attempts += 1
        if user_guess == secret_word:
            return attempts
def ask(prompt: str, valid: list[str] = None) -> str:
    '''
    Recursive function for varification of typed word: is it in the dictionary
    (valid) or not
    '''
    print(cowsay(prompt, MY_COW))
    player_guess = input('\033[92m'+'>> '+'\033[0m')
    if player_guess in valid:
        return player_guess
    print('\033[93m'+'Unknown word! Try again'+'\033[0m')
    return ask(prompt, valid)

def inform(format_string: str, bulls: int, cows: int) -> None:
    fstr = format_string.format(bulls, cows)
    print(fstr)

def download_words(url):
    '''
    Pull data from url
    '''
    filename = "words.txt"
    urllib.request.urlretrieve(url, filename)
    return filename

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m bullscows <dictionary> [length]")
        return

    dictionary = sys.argv[1]
    length = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    if dictionary.startswith("http"):
        filename = download_words(dictionary)
    else:
        filename = dictionary

    with open(filename, 'r', encoding='utf-8') as file:
        words = [word.strip() for word in file if len(word.strip()) == length]

    attempts = gameplay(ask, inform, words)
    print("Congratulation!\nUsed attempts", attempts)

if __name__ == "__main__":
    main()
