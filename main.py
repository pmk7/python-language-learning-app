import os
import random
import json
from datetime import datetime
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
            self.vocab_meta = {}
            self.save_vocab()
        else:
            self.load_vocab()

    def load_vocab(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.vocab = data.get('vocab', [])
            self.vocab_meta = data.get('meta', {})

    def save_vocab(self):
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump({'vocab': self.vocab, 'meta': self.vocab_meta},
                      file, indent=4, ensure_ascii=False)

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
        self.words_today = self.vocab_meta.get('words_today', 0)
        self.last_update = datetime.strptime(self.vocab_meta.get(
            'last_update', datetime.now().date().isoformat()), '%Y-%m-%d').date()

    def can_add_word(self):
        today = datetime.now().date()
        if today > self.last_update:
            self.words_today = 0
            self.last_update = today

        return self.words_today < 3

    def add_word(self, german, english):
        if not self.can_add_word():
            print("You can only add 3 words per day.")
            return

        super().add_word(german, english)
        self.words_today += 1
        self.update_meta_data()

    def update_meta_data(self):
        self.vocab_meta['words_today'] = self.words_today
        self.vocab_meta['last_update'] = self.last_update.isoformat()
        self.save_vocab()


class PremiumUser(BaseUser):
    def __init__(self, username, filepath):
        super().__init__(username, filepath)

    def __str__(self):
        return f"Premium User: {self.username}, Vocab: {len(self.vocab)}"


class Quiz:
    def __init__(self, vocab, user, is_dictionary_quiz=False):
        """ Initializes the Quiz object

        Args:
            vocab (list): List of words to be used in the quiz.
            user (User): User playing the quiz.
        """
        self.vocab = vocab
        self.user = user
        self.is_dictionary_quiz = is_dictionary_quiz

        print(f"Welcome to the German Quiz!\n")

    def random_word(self):
        """ Selects a random word from the vocabulary and quizzes the user """
        # Generate a random number within the range of the vocabulary length
        random_num = random.randint(0, len(self.vocab) - 1)
        random_word = self.vocab[random_num]
        ger_word = random_word.get('german')

        # Test if the API is working
        test = SentenceGenerator(api_key)
        api_test = test.test_api('haus')

        # Prompt user for an answer with a hint option if API is working
        if api_test:
            answer = input(
                f"What is the English translation of {ger_word}? Press 'h' for a hint:  \n")
        else:
            answer = input(
                f"What is the English translation of {ger_word}? \n")

        # Provide a hint if the user inputs 'h' and API is working
        if answer == 'h' and api_test:
            word = SentenceGenerator(api_key)
            print(word.generate_sentence(ger_word) + "\n")
            answer = input("Answer: ")

        # Check the user's answer
        if answer == random_word.get('english'):
            print("\nCorrect! ⭐️ \n")

        elif answer != random_word.get('english'):
            print("Incorrect! Answer: " + random_word.get("english") +
                  "\n" + "Would you like to add this word to your dictionary?")

            # Check if the user is playing the dictionary quiz
            if not self.is_dictionary_quiz:
                # Prompt user to add the word to their dictionary
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
        """Initializes the Menu object

        Args: 
        user (User): User playing the quiz. 
        vocab (list): List of words to be used in the quiz 
        """
        self.user = user
        self.vocab = vocab

        print(f"\nWelcome {user.username} to your Language App!\n")

        while True:
            # Display menu options
            print("\n1. Quiz\n")
            print("\n2. Edit my Dictionary\n")
            print("\n3. Study My Dictionary\n")
            print("\n4. Quit\n")

            choice = input("What would you like to do? Select a number: ")

            # Quiz with all words
            if choice == '1':
                if isinstance(user, RegularUser) and not user.can_add_word():
                    print(
                        "You can only add 3 words per day. Please try again tomorrow or upgrade to Premium.")
                else:
                    game1 = Quiz(my_words, user)
                    game1.random_word()

            # Edit user's dictionary
            elif choice == '2':
                user.print_my_vocab()
                print("\nDo you want to add or delete words from your dictionary?\n")
                edit_choice = input(
                    "Type 'add' to add words, 'delete' to delete words or 'back' to return to the menu: ")

                while edit_choice not in ['add', 'delete', 'back']:
                    edit_choice = input(
                        "Invalid choice. Type 'add' to add words, 'delete' to delete words or 'back' to return to the menu: ")

                # Add words to the user's dictionary
                if edit_choice == 'add':
                    german_word = input("Enter the German word: ")
                    english_word = input("Enter the English translation: ")
                    if user.add_word(german_word, english_word) != False:
                        print(
                            "You've reached the limit of 3 words per day. Please try again tomorrow or upgrade to Premium.")
                    else:
                        user.add_word(german_word, english_word)
                        print(
                            f"Added {german_word} ({english_word}) to your dictionary.")

                # Delete words from the user's dictionary
                elif edit_choice == 'delete':
                    german_word = input(
                        "Enter the German word you want to remove: ")
                    user.remove_word(german_word)
                    print(f"Removed {german_word} from your dictionary.")

                # Return to the main menu
                elif edit_choice == 'back':
                    continue

            # Quiz with the user's dictionary words
            elif choice == '3':
                if len(user.vocab) == 0:
                    print(
                        "Your dictionary is empty. Add words to your dictionary before studying.")
                else:
                    game2 = Quiz(user.vocab, user, is_dictionary_quiz=True)
                    game2.random_word()

            # Quit the application
            elif choice == '4':
                quit()

            # Invalid menu choice
            else:
                print("Invalid choice. Please try again.")
                continue


john = RegularUser("John", data_directory)
sarah = PremiumUser("Sarah", data_directory)


# player1 = Menu(john, my_words)  # For a regular users
player2 = Menu(sarah, my_words)  # For a premium user
