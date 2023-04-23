import os
import random
from sen_gen import SentenceGenerator
from data import *

api_key = os.getenv("OPENAI_API_KEY")
selected_word_example = SentenceGenerator(api_key)

class Quiz:
  def __init__(self, vocab):
    self.vocab = vocab
    
    print("Welcome to the German Quiz!")
    
  def random_word(self):
    random_num = random.randint(0, len(self.vocab) - 1)
    random_word = self.vocab[random_num]
    ger_word = random_word.get('german')
    
    answer = input(f"What is the English translation of {ger_word}? Press 'h' for a hint:  ")
    
    if answer == 'h':
      word = SentenceGenerator(api_key)
      print(word.generate_sentence(ger_word))
      answer = input("Answer: ")
      
    if answer == random_word.get('english'):
      print("Correct!")
    elif answer != random_word.get('english'):
      print("Incorrect! Answer: " + random_word.get("english"))   
    else:
      quit()  
      
  
    
    
class Dictionary:
  def __init__(self, vocab):
    self.vocab = vocab
    
    def add(self):
      pass
    
    def remove(self):
      pass
    
    
class Flascard:
  pass
    
class Player:
  pass


class Menu:
  def __init__(self, vocab):
    self.vocab = vocab
    
    print("Welcome to the German Quiz!")
    
    while True:
      print("1. Quiz")
      print("2. Update Dictionary")
      print("3. Quit")
      
      choice = input("What would you like to do? ")
      
      if choice == '1':
        game1 = Quiz(my_words)   
        game1.random_word()
      elif choice == '2':
        pass
      elif choice == '3':
        quit()
      else:
        print("Invalid choice. Please try again.")
        continue
      
      

  
  

player1 = Menu(my_words)      