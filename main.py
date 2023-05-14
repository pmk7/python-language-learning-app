import os
import random
import json
import re
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
        self.vocab_set = set()

        if not os.path.exists(self.filepath):
            self.vocab = []
            self.vocab_meta = {}
            self.save_vocab()
        else:
            self.load_vocab()

    def load_vocab(self):
        """Loads vocabulary from the JSON file"""
        with open(self.filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.vocab = data.get('vocab', [])
            self.vocab_meta = data.get('meta', {})
            # Populate vocab_set with words from vocab
            self.vocab_set = {word['german'] for word in self.vocab}

    def save_vocab(self):
        """Saves vocabulary to the JSON file"""
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump({'vocab': self.vocab, 'meta': self.vocab_meta},
                      file, indent=4, ensure_ascii=False)

    def print_my_vocab(self):
        """Prints the user's vocabulary"""
        print(self.vocab)

    def find_word(self, german):
        """Finds a word in the user's vocabulary"""
        word = [i for i in self.vocab if i['german'] == german]
        if word:
            return word[0]
        return

    def add_word(self, german, english):
        """Adds a word to the user's vocabulary"""
        if german in self.vocab_set:
            print('Already contained!')
            return False

        else:
            word_id = len(self.vocab) + 1
            word = {'id': word_id, 'german': german,
                    'english': english}
            self.vocab.append(word)
            self.vocab_set.add(german)
            self.save_vocab()

    def remove_word(self, german):
        """Removes a word from the user's vocabulary"""
        word = self.find_word(german)
        if word:
            self.vocab.remove(word)
            self.vocab_set.remove(german)
            self.save_vocab()

    def update_my_vocab(self, german, english):
        """Updates the user's vocabulary"""
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
        """Checks if the user can add more words to their vocabulary today"""
        today = datetime.now().date()
        if today > self.last_update:
            self.words_today = 0
            self.last_update = today

        return self.words_today < 3

    def add_word(self, german, english):
        """Adds a word to the user's vocabulary, respecting the daily limit"""
        if not self.can_add_word():
            print("You can only add 3 words per day")
            return

        super().add_word(german, english)
        self.words_today += 1
        self.update_meta_data()

    def update_meta_data(self):
        """Updates the metadata for the user's vocabulary"""
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
        """
        Initializes the Quiz object.

        Args:
            vocab (list): List of words to be used in the quiz.
            user (User): User playing the quiz.
            is_dictionary_quiz (bool, optional): Flag to indicate if it's a dictionary quiz. Defaults to False.
        """
        self.vocab = vocab
        self.user = user
        self.is_dictionary_quiz = is_dictionary_quiz

    def normalize_answer(self, answer):
        """
        Normalizes the answer by removing unnecessary characters and spaces.

        Args:
            answer (str): The user's answer.

        Returns:
            str: The normalized answer.
        """
        # Remove 'to ' from the beginning of the answer
        answer = re.sub(r'^to\s', '', answer)

        # Remove square brackets and their content
        answer = re.sub(r'\[.*?\]', '', answer)

        # Remove curly brackets and their content
        answer = re.sub(r'\{.*?\}', '', answer)

        # Remove regular brackets and their content
        answer = re.sub(r'\(.*?\)', '', answer)

        # Remove leading and trailing spaces
        answer = answer.strip()

        return answer

    def random_word(self):
        """
        Selects a random word from the vocabulary and quizzes the user.
        """
        while True:
            # Generate a random number within the range of the vocabulary length
            random_num = random.randint(0, len(self.vocab) - 1)
            random_word = self.vocab[random_num]
            ger_word = random_word.get('german')

            # Test if the API is working
            test = SentenceGenerator(api_key)
            api_test = test.test_api('test')

            # Prompt user for an answer with a hint option if API is working
            if api_test:
                answer = input(
                    f"What is the English translation of {ger_word}? Press 'h' for a hint or 's' to skip or 'b' to go back to menu:  \n")
            else:
                answer = input(
                    f"What is the English translation of {ger_word}? Press 's' to skip or 'b' to go back to menu: \n")

            # Handle user's decision to skip the word
            if answer.lower() == 's':
                if len(self.vocab) > 1:
                    print("Answer: " + random_word.get('english'))
                    print("Skipping this word.\n")
                    continue
                else:
                    print(
                        "You have no words in your dictionary to skip to. Please add words to your dictionary.\n")
                    break

            # Provide a hint if the user inputs 'h' and API is working
            if answer.lower() == 'h' and api_test:
                word = SentenceGenerator(api_key)
                print(word.generate_sentence(ger_word) + "\n")
                answer = input("Answer: ")

            if answer.lower() == 'b':
                return 'back_to_menu'

            # Check the user's answer
            normalized_answer = self.normalize_answer(answer)
            normalized_correct_answer = self.normalize_answer(
                random_word.get('english'))

            if normalized_answer == normalized_correct_answer:
                print("\nCorrect! ⭐️ \n")
            elif normalized_answer != normalized_correct_answer and self.is_dictionary_quiz:
                print('\nIncorrect! Answer: ' + random_word.get('english'))
            else:
                print("\nIncorrect! Answer: " + random_word.get("english") +
                      "\n" + "Would you like to add this word to your dictionary?")

                user_input = input("Press 'y' for yes and 'n' for no: ")
                while user_input not in ['y', 'n']:
                    print("Invalid input. Please enter 'y' for yes or 'n' for no.")
                    user_input = input("Press 'y' for yes and 'n' for no: ")

                if user_input == 'y' and self.user.can_add_word():
                    self.user.add_word(ger_word, random_word.get('english'))
                    print("Word added!")
                elif user_input == 'y' and not self.user.can_add_word():
                    print("You can only add 3 words per day")
                elif user_input == 'n':
                    print("Word not added!")

                continue


class Menu:
    def __init__(self, user, vocab):
        """Initializes the Menu object

        Args: 
        user (User): User playing the quiz
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

            choice = input(
                f"What would you like to do, {user.username} ? Select a number: ")

            # Quiz with all words
            if choice == '1':
                if isinstance(user, RegularUser) and not user.can_add_word():
                    print(
                        "You can only add 3 words per day. Please try again tomorrow or upgrade to Premium.")
                else:
                    game1 = Quiz(my_words, user)
                    result = game1.random_word()
                    if result == 'back_to_menu':
                        continue

            # Edit user's dictionary
            elif choice == '2':
                user.print_my_vocab()
                print("\nDo you want to add or delete words from your dictionary?\n")
                edit_choice = input(
                    "Type 'add' to add words, 'del' to delete words or 'b' to return to the menu: ")

                while edit_choice not in ['add', 'del', 'b']:
                    edit_choice = input(
                        "Invalid choice. Type 'add' to add words, 'del' to delete words or 'b' to return to the menu: ")

                # Add words to the user's dictionary
                if edit_choice == 'add':
                    german_word = input("Enter the German word: ")
                    english_word = input("Enter the English translation: ")
                    if isinstance(user, RegularUser) and not user.can_add_word():
                        print(
                            "You've reached the limit of 3 words per day. Please try again tomorrow or upgrade to Premium.")
                    else:
                        user.add_word(german_word, english_word)
                        print(
                            f"Added {german_word} ({english_word}) to your dictionary.")

                # Delete words from the user's dictionary
                elif edit_choice == 'del':
                    german_word = input(
                        "Enter the German word you want to remove: ")
                    if user.remove_word(german_word) == False:
                        print(
                            f"{german_word} is not in your dictionary. Please try again.")
                    else:
                        user.remove_word(german_word)
                        print(f"Removed {german_word} from your dictionary.")

                # Return to the main menu
                elif edit_choice == 'b':
                    continue

            # Quiz with the user's saved dictionary words
            elif choice == '3':
                if len(user.vocab) == 0:
                    print(
                        "Your dictionary is empty. Add words to your dictionary before studying.")
                else:
                    game2 = Quiz(user.vocab, user, is_dictionary_quiz=True)
                    game2.random_word()

            # Quit the application
            elif choice == '4':
                break

            # Invalid menu choice
            else:
                print("Invalid choice. Please try again.")
                continue


# john = RegularUser("John", data_directory)
# sarah = PremiumUser("Sarah", data_directory)


# player1 = Menu(john, my_words)  # For a regular users
# player2 = Menu(sarah, my_words)  # For a premium user
