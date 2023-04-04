import os
import openai
from data import *

class SentenceGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def generate_sentence(self, word, max_tokens=75, temperature=0.9):
        prompt = f"Ein Beispiel mit: {word}"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=[".", "!", "?"]
        )

        response_text = response.get('choices')[0].get('text')
        return response_text.strip()

# Usage example:

# api_key = os.getenv("OPENAI_API_KEY")
# selected_word_example = SentenceGenerator(api_key)

# word = 'Handy'
# generated_sentence = selected_word_example.generate_sentence(word)

# print(generated_sentence)

  