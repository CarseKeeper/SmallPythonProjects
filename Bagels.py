import random

NUM_DIGITS:int = 3
MAX_GUESSES:int = 10

def main():
    print('''Welcome to Bagels!\nI am thinking of a {}-number code without repeated digits
          Here are some hints to help with your Guessing:
          When I say:       That means:
            Pico                One digit is correct but in the wrong position
            Fermi               One digit is correct and in the correct position
            Bagels              No digit is correct
            E.X.
            If the number was 248 and you guessed 498, the clue would be Fermi Pico'''.format(NUM_DIGITS))
    
    while True:     #Game loop
        secretNumber:str = getSecretNumber()
        print('I have thought of a number.\nYou have {} guesses to get it.'.format(MAX_GUESSES))
        
        numGuesses:int = 1
        while numGuesses <= MAX_GUESSES:
            guess:str = ''
            while len(guess) != NUM_DIGITS or not guess.isdecimal():
                print('Guess #{}: '.format(numGuesses))
                guess = input('> ')
                
            clues:str = getClues(guess, secretNumber)
            print(clues)
            numGuesses += 1
            
            if guess == secretNumber:
                break
            if numGuesses > MAX_GUESSES:
                print('You ran out of guesses.')
                print('The answer was {}.'.format(secretNumber))
                
        print('Do you want to play again? (yes/no)')
        if not input('> ').lower().startswith('y'):
            break
    print('Thanks for playing!')
    
    def getSecretNumber() -> str:
        #returns a string of ints of length NUM_DIGITS unique random digits.
        numbers = list('0123456789')
        