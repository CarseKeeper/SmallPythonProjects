import random
import os

NUM_DIGITS:int = 3      #! try changing this for a different length code (Must be greater than 0 and less than or equal to 10)
MAX_GUESSES:int = 10     #! try changing this for more/less guesses (Must be greater than 0)

def main():
    #Clears the terminal of both Windows and Linux systems
    if(os.system('cls') != 0):
        os.system('clear')
    
    #Introduction and rules of the game
    print('''Welcome to Bagels!\nI am thinking of a {}-digit code without repeated digits\n\nHere are some hints to help with your Guessing:
    When I say:       That means:
        Pico                One digit is correct but in the wrong position
        Fermi               One digit is correct and in the correct position
        Bagels              No digit is correct
E.X.
If the number was 248 and you guessed 498, the clue would be Fermi Pico'''.format(NUM_DIGITS))
    
    while True:     #Game loop
        secretNumber: str = getSecretNumber()
        print('\nI have thought of a number.\nYou have {} guesses to get it.'.format(MAX_GUESSES))
        
        #Loop for guessing the current secret code
        numGuesses:int = 1
        while numGuesses <= MAX_GUESSES:
            guess:str = ''
            while len(guess) != NUM_DIGITS or not guess.isdecimal(): #Checks if the guess is NUM_DIGITS long or a number at all
                print('\nGuess #{}: '.format(numGuesses))
                guess = input('> ')
            
            #Calls method to get the list of clues for the guess
            clues:str = getClues(guess, secretNumber)
            print(clues)
            numGuesses += 1
            
            if guess == secretNumber: #Break out of loop if correct or out of guesses
                break
            if numGuesses > MAX_GUESSES:
                print('You ran out of guesses.')
                print('The answer was {}.'.format(secretNumber))
                
        #Ask if player would like to start another round, if not, end
        print('\nDo you want to play again? (yes/no)')
        if not input('> ').lower().startswith('y'):
            break
        if(os.system('cls') != 0):
                os.system('clear')
    print('Thanks for playing!') #Always be curteous
    
    
def getSecretNumber() -> str:
    #Returns a string of ints of length NUM_DIGITS unique random digits.
    numbers: list[str] = list('0123456789')
    random.shuffle(numbers) #Randomizes the list of digits
    secretNumber:str = ''
    for i in range(NUM_DIGITS):
        secretNumber += numbers[i]
    return secretNumber
    
def getClues(guess, secretNumber) -> str:
    if guess == secretNumber:
        return 'You got it!'
    
    clues: list[str] = []
    
    for i in range(len(guess)): #For loop checks all digits in guess
        if guess[i] == secretNumber[i]: #If digit is fully correct, add a Fermi
            clues.append('Fermi')
        elif guess[i] in secretNumber: #If digit is in wrong spot, add a Pico
            clues.append('Pico')    
    if len(clues) == 0: #If no digit is remotely correct, return Bagels, Mmmm bagels
        return 'Bagels'
    else:
        clues.sort() #Alphabetically sort the clues to make the clues slightly less helpful
        return ''.join(clues)
        
        
if __name__ == '__main__': #Checks for if package was imported rather than taken as a whole
    main()