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
    def __init__(self, username, filepath):
        self.username = username
        self.filepath = f"{filepath}/{self.username}.json"

        if not os.path.exists(self.filepath):
            self.vocab = []
            self.save_vocab()
        else:
            self.load_vocab()

    def load_vocab(self):
        with open(self.filepath, 'r') as file:
            self.vocab = json.load(file)

    def save_vocab(self):
        with open(self.filepath, 'w') as file:
            json.dump(self.vocab, file)

    def print_my_vocab(self):
        print(self.vocab)

    def find_word(self, german):
        print(self.vocab)
        for word in self.vocab:
            if word['german'] == german:
                return word
        return None

    def add_word(self, german, english):
        if self.find_word(german):
            print('Already contained!')
        else:
            word_id = len(self.vocab) + 1
            word = {'id': word_id, 'german': german,
                    'english': english, 'correct': 0, 'incorrect': 0}
            self.vocab.append(word)
            self.save_vocab()

    def remove_word(self, german):
        word = self.find_word(german)
        if word:
            self.vocab.remove(word)
            self.save_vocab()

    def update_my_vocab(self, german, english):
        word_id = len(self.vocab) + 1
        word = {'id': word_id, 'german': german,
                'english': english, 'correct': 0, 'incorrect': 0}
        self.save_vocab()

    def __str__(self):
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

        # Test api is working
        test = SentenceGenerator(api_key)

        answer = input(
            f"What is the English translation of {ger_word}? Press 'h' for a hint:  \n")

        # If Api isn't working, handle issue before it breaks code. Let user continue to play quiz without hint feature.
        if answer == 'h' and test == True:
            # ! Look into this more, instantiating object within another object
            word = SentenceGenerator(api_key)
            print(word.generate_sentence(ger_word) + "\n")
            answer = input("Answer: ")
        answer = input(
            "Sorry, the hint feature is't available right now. What is your answer: ")

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
            print("\n3. Study My Dictionary\n")
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
# print(regular_user)
# print(premium_user)
# print(regular_user.print_my_vocab())
# regular_user.add_word("Handy", "phone")
# regular_user.remove_word("Haus")


player1 = Menu(regular_user, my_words)  # For a regular user


# print(player1)
# or
# player1 = Menu(premium_user, my_words)  # For a premium user
