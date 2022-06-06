import random


print("H A N G M A N")


class Hangman:

    def __init__(self):

        self.attempts = 8
        self.set_of_letters = None
        self.words = ["java", "python", "swift", "javascript" ]
        self.duplicates = []
        self.won_games = 0
        self.lost_games = 0

    #Making random choice in set
    def random_choice(self):
        self.random_word = (random.choice(self.words))
        self.set_of_letters = list("-" * len(self.random_word))
        return self.random_word

    #printing all information and checking if we guess the hidden word
    def printing_word(self, right_letter = None):
        if right_letter in self.set_of_letters:
            print("You've already guessed this letter")
            print()
            print("".join(self.set_of_letters))
        else:
            print()
            for index in range(len(self.random_word)):
                if self.random_word[index] == right_letter:
                    self.set_of_letters[index] = right_letter
            print("".join(self.set_of_letters))
            #check if we guess the word
            if "".join(self.set_of_letters) == self.random_word:
                print(f"You guessed the word {self.random_word}!\nYou survived!")
                self.end_game('won')


    def input_check(self):
        while True:
            player_input = input("Input a letter: ")
            if len(player_input) != 1:
                print("Please, input a single letter.")
                self.printing_word()
            elif player_input not in 'qwertyuiopasdfghjklzxcvbnm':
                print("Please, enter a lowercase letter from the English alphabet.")
                self.printing_word()
            elif player_input in self.duplicates:
                print("You've already guessed this letter.")
                self.printing_word()
            else:
                self.duplicates.append(player_input)
                return player_input


    def menu(self):
        player_input = input('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit:')
        if player_input == 'play':
            self.duplicates = []
            self.main()
        elif player_input == 'results':
            print(f"You won: {self.won_games} times.\nYou lost: {self.lost_games} times.")
            self.menu()
        elif player_input == 'exit':
            quit()

    def end_game(self, result):
        if result == 'won':
            self.won_games += 1
        elif result == 'lost':
            self.lost_games += 1
        self.menu()

    def main(self):
        random_word = self.random_choice()
        self.printing_word()
        while self.attempts > 0:
            player_guess = self.input_check()
            if player_guess in random_word:
                self.printing_word(player_guess)

            else:
                print("That letter doesn't appear in the word.")
                self.attempts -= 1
                self.printing_word()
        print("You lost!")
        self.end_game('lost')


hangman = Hangman()
hangman.menu()
