import os
import random
import json
from sen_gen import SentenceGenerator
from data import *

api_key = os.getenv("OPENAI_API_KEY")
selected_word_example = SentenceGenerator(api_key)

data_directory = "user_data"
if not os.path.exists(data_directory):
    os.makedirs(data_directory)


class BaseUser:
    """A base class for users. Handles vocabulary management and storage."""

    def __init__(self, username, filepath):
        """Initialize a user with a username and a file path for storing vocabulary."""
        self.username = username
        self.filepath = f"{filepath}/{self.username}.json"

        if not os.path.exists(self.filepath):
            self.vocab = []
            self.save_vocab()
        else:
            self.load_vocab()

        def load_vocab(self):
            """Load the user's vocabulary from a JSON file."""
            with open(self.filepath, 'r') as file:
                self.vocab = json.load(file)

        def save_vocab(self):
            """Save the user's vocabulary to a JSON file."""
            with open(self.filepath, 'w') as file:
                json.dump(self.vocab, file, ensure_ascii=False)

        def print_my_vocab(self):
            """Print the user's vocabulary."""
            print(self.vocab)

        def find_word(self, german):
            """Find a word in the user's vocabulary by its German form."""
            print(self.vocab)
            for word in self.vocab:
                if word['german'] == german:
                    return word
                return None

        def add_word(self, german, english):
            """Add a word to the user's vocabulary."""
            if self.find_word(german):
                print('Already contained!')
            else:
                word_id = len(self.vocab) + 1
                word = {'id': word_id, 'german': german,
                        'english': english, 'correct': 0, 'incorrect': 0}
                self.vocab.append(word)
                self.save_vocab()

        def remove_word(self, german):
            """Remove a word from the user's vocabulary by its German form."""
            word = self.find_word(german)
            if word:
                self.vocab.remove(word)
                self.save_vocab()

        def update_my_vocab(self, german, english):
            """Update the user's vocabulary with a new word."""
            word_id = len(self.vocab) + 1
            word = {'id': word_id, 'german': german,
                    'english': english, 'correct': 0, 'incorrect': 0}
            # Fix problem. Add incorrect word to users dictionary

        def __str__(self):
            """Return a string representation of the user."""
            return f"User: {self.username}, Vocab: {len(self.vocab)}"


class RegularUser(BaseUser):
    def __init__(self, username, filepath):
        super().__init__(username, filepath)
        self.quiz_rounds = 3

    def __str__(self):
        return f"Regular User: {self.username}, Vocab: {len(self.vocab)}"


class PremiumUser(BaseUser):
    def __init__(self, username, filepath):
        super().__init__(username, filepath)
        self.quiz_rounds = 5

    def __str__(self):
        return f"Premium User: {self.username}, Vocab: {len(self.vocab)}"


class Dictionary(BaseUser):
    def __init__(self, username, filepath):
        super().__init__(username, filepath)


class Quiz:
    def __init__(self, vocab, user):
        self.vocab = vocab
        self.user = user

        print("Welcome to the German Quiz!\n")

    def random_word(self):
        random_num = random.randint(0, len(self.vocab) - 1)
        random_word = self.vocab[random_num]
        ger_word = random_word.get('german')

        answer = input(
            f"What is the English translation of {ger_word}? Press 'h' for a hint:  \n")

        if answer == 'h':
            word = SentenceGenerator(api_key)
            print(word.generate_sentence(ger_word) + "\n")
            answer = input("Answer: ")

        if answer == random_word.get('english'):
            print("Correct!")
        elif answer != random_word.get('english'):
            print("Incorrect! Answer: " + random_word.get("english") +
                  "\n" + "Would you like to add this word to your dictionary?")

            userInput = input("Press 'y' for yes and 'n' for no: ")
            if userInput == 'y':
                self.user.add_word(ger_word, random_word.get('english'))
                print("Word added!")
            elif userInput == 'n':
                print("Word not added!")
        else:
            quit()


class Menu:
    def __init__(self, user, vocab):
        self.user = user
        self.vocab = vocab

        print("\nWelcome to your Language App!\n")

        while True:
            print("\n1. Quiz\n")
            print("\n2. Edit my Dictionary\n")
            print("\n3. Revise My Dictionary\n")
            print("\n4. Quit\n")

            choice = input("What would you like to do? Select a number: ")

            if choice == '1':
                game1 = Quiz(my_words, user)
                game1.random_word()
            elif choice == '2':
                pass
            elif choice == '3':
                pass
            elif choice == '4':
                quit()
            else:
                print("Invalid choice. Please try again.")
                continue


regular_user = RegularUser("John", data_directory)
premium_user = PremiumUser("Sarah", data_directory)
print(regular_user)
print(premium_user)
print(regular_user.print_my_vocab())
# regular_user.add_word("Handy", "phone")
regular_user.remove_word("Haus")


player1 = Menu(regular_user, my_words)  # For a regular user


# print(player1)
# or
# player1 = Menu(premium_user)  # For a premium user
