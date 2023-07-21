from random import randint

"""
This program is a self made version of the Hangman program contained in Al Sweigart's book,
Invent Your Own Computer Games With Python.
Essentially, the code in the book was scanned over, then this program was written
adhering to the idea, but without reference to the book code.
It was a learning exercise. There are, as a consequence, some differences.
Python 3.11.4, on Xubuntu 22.04.
20 July, 2023, William Shearer
"""

WORD_COUNT = 50
TRIES = 6
ALPHA = "abcdefghijklmnopqrstuvwxyz"
IMAGE = [
"""
|----
|    
|    
|    
|    
=====
""",
"""
|----
|  O 
|    
|    
|    
=====
""",
"""
|----
|  O 
|  | 
|    
|    
=====
""",
"""
|----
|  O 
| /| 
|    
|    
=====
""",
"""
|----
|  O
| /|\\
|    
|    
=====
""",
"""
|----
|  O 
| /|\\
| /  
|    
=====
""",
"""
|----
|  O 
| /|\\
| / \\
|    
=====
"""]

def get_words():
    """
    This is only used once per program run.
    It loads a list of strings from a text file.
    From that, a smaller list is created, of WORD_COUNT length.
    The list is returned to the main loop.
    """
    with open("nouns.txt", "r") as text_file:
        all_words = text_file.read().split()
        
    words = list()
    for _ in range(WORD_COUNT):
        words.append(all_words[randint(0, len(all_words) - 1)])

    return words


def select_word(words):
    """
    Three things are done here.
    First, a word from the list of words is selected for the game.
    A random index is generated to do this. That same index is used
    to then delete the word from the list (which, as a list, behaves globally).
    The word (which is a string) is then broken up into a list of chars
    with a list comprehension, and returned to the game_loop that way.
    """
    w_index = randint(0, len(words) - 1)
    word = words[w_index]
    del words[w_index]
    
    return [c for c in word]
    # return [c for c in words[randint(0, len(words) - 1)]]


def display(hits, misses, p_word, g_char, word):
    """
    This first displays the ASCII art, based on how many misses there have been.
    Then, the player_word is displayed (which is the partially made word,
    with blanks, unless it has been completed, of course).
    If the number of hits, one of which is awarded in the game loop for
    every letter that is asserted in the word, equals the length of the
    secret word, then it means the word was completed. You Win is displayed.
    If the number of misses equals the number of TRIES, then it means the
    game is lost. In both cases the game_loop should not continue.
    WIN is returned if the round is won, and LOSE if lost, otherwise
    CONTINUE is returned (redundantly) so that the round can continue.
    This condition is evaluated in a match case inside the game_loop.
    """
    print(IMAGE[misses])

    print_player_word(p_word, g_char)
    if hits == len(word):
        print("You win!")
        return "WIN"
    elif misses == TRIES:
        print("You lose!")
        print(f"The word was {''.join(word).upper()}.")
        return "LOSE"
    else:        
        return "CONTINUE"


def print_player_word(p_word, g_char):
    """
    Simple enough. The main take away here is the use of
    join() to create a string out of the list. This is the
    player word.
    Here, the list of already used letters is also displayed.
    """
    print(" ".join(p_word).upper())
    print("\nUsed letters: " + g_char.upper())



def game_loop(word):
    """
    The game loop. While the player word is neither complete or the misses
    have not met the allowed number of tries (governed by display), the loop
    continues.
    The player is asked to input a letter.
    The logic controls some conditions for an acceptable input:
    It should only be 1 character long.
    It should be in the ALPHA string (a letter of the alphabet).
    It should not have already been used.
    If it has not been used, it is added to the used character list.
    It is then checked to determine if it is in the word, and if it is,
    it is then checked to verify how many times.
    Where it occurs in the word, it is added to the player_word, in
    the correct position (index), by comparison to the secret word.
    The hits variable is increased for each time the letter is placed
    into the word.
    If the letter is not in the word, then the misses variable is increased.
    If the loop is broken, display has already printed the appropriate message.
    """
    # Locals
    hits = 0
    misses = 0
    guessed_characters = ""
    evaluate = ""
    player_word = ["_" for c in range(len(word))]
    print("\nHANGMAN\n")
    # Game loop
    while True:
        # if not display(hits, misses, player_word, guessed_characters, word):
        #    break
        """
        Every time display is called, it will return a value to the
        variable evaluate, which is then checked in the match case.
        If the game is either won or lost, this function is broken out
        of returning either True or False, respectively.
        In the main loop, that value is utilized to determine the number
        of time the user asserted a word or lost the round.
        The score is given when the rounds end.
        """
        evaluate = display(hits, misses, player_word, guessed_characters, word)

        match evaluate:
            case "WIN":
                return True
            case "LOSE":
                return False
            case other:
                pass
             
        guess = input("Guess a letter: ").lower()
        if len(guess) == 1:
            if guess in ALPHA:
                if guess not in guessed_characters:
                    guessed_characters += guess
                    if guess in word:
                        print("\nGood job!")
                        for i, c in enumerate(word):
                            if guess == c:
                                player_word[i] = c
                                hits += 1
                    else:
                        misses += 1
                        print(f"\nThe letter {guess.upper()} is not in the word.")
                else:
                    print(f"\nYou already used {guess.upper()}.")
            else:
                print("\nUse alphabet characters only.")
        else:
            print("\nUse a single letter only.")


def main():
    """
    Main has its own loop. The loop is infinate, and broken by conditions
    that either the player creates (pressing N) or the game dictates
    (all the words in the list have been used).
    The main loop gets a word from select_word function, and is passed the
    list of string words to get the word for the game.
    That word is passed to the game_loop.
    """
    # used_words = list()
    words = get_words()
    won = 0
    lost = 0
    while True:
        # selected word comes back as a list, not a string.
        word = select_word(words)
        # used_words.append("".join(word))

        if game_loop(word):
            won += 1
        else:
            lost += 1

        if len(words) > 0:
            play_again = input("Play again? (Y or N): ").lower()
            if play_again[0] == "n":        
                break
        else:
            print(f"You have played {WORD_COUNT} words. \nTake a break now and play again later!")
            break
        
    print(f"\nYou scored {won} wins out of {won + lost} rounds.")
    print("\nThanks for playing!")
        

if __name__ == "__main__":
    main()





"""
nouns.txt
textfile = open("nouns.txt", "a")
for word in WORDS:
    if len(word) > 4 and len(word) < 11:
        textfile.write(word + " ")

textfile.close()
"""
    
        


    
