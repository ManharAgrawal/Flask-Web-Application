import random

def word_guessing_game(): 
    def display_word(word, guessed_letters):
        display = []
        for letter in word:
            if letter in guessed_letters:
                display.append(letter)
            else:
                display.append('_')
        return ' '.join(display)
    
    words = ["lemon", "mango", "banana", "apple", "bugati", "mclaren", "lagoon", "optimus", "autobots", "newyork"]
    name = input("Enter your name: ")
    print(f"Hi {name}, let's start the game")

    print("\n\t ***Word Guessing Game*** ")
    print("\n You have 10 attempts to guess the word correctly.")
    
    wrong_list = []
    original_word = random.choice(words)
    guessed_word = []
    for _ in original_word:
        guessed_word.append('_')

    attempts = 10
    while attempts:
        print(display_word(original_word, guessed_word))        
        guessed_letter = input("Guess a letter: ").lower()
        
        if not guessed_letter.isalpha() or len(guessed_letter) != 1:
            print('Please guess a single letter.')
            continue
        
        if guessed_letter in wrong_list:
            print('You have already guessed this letter.')
            continue

        if guessed_letter in original_word:
            for i in range(len(original_word)):
                if original_word[i] == guessed_letter:
                    guessed_word[i] = guessed_letter
        else:
            print("Incorrect guess.")
            wrong_list.append(guessed_letter)

        if original_word == ''.join(guessed_word):
            print(f'Congratulations! You guessed the word: {original_word}')
            return

        attempts -= 1
        print(f"You have {attempts} attempts left.")

    print(f"You ran out of attempts. The word was {original_word}")

word_guessing_game()