import json


def read_vocab_file(filepath):
    """
    Reads a file at a given filepath and returns the content line by line.

    Args:
        filepath (str): Path of the file to be read.

    Returns:
        list: List of lines read from the file.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.readlines()
    return content


def convert_txt_to_vocab_list(filepath):
    """
    Reads a vocabulary file and converts it to a list of word dictionaries.

    Args:
        filepath (str): Path of the vocabulary file.

    Returns:
        list: List of dictionaries where each dictionary represents a word with its German and English translations.
    """
    my_words = []

    try:
        # Read the content of the file
        content = read_vocab_file(filepath)

        # Remove unnecessary characters
        adjusted_content = [x.strip().replace(
            "\t", " : ").replace('.', '') for x in content]

        for i, word in enumerate(adjusted_content):
            # Skip empty lines
            if not word.strip():
                continue

            # Assign an ID to each word
            word_id = i + 1

            # Split each line into English and German words
            eng_word, ger_word = word.split(" : ")

            # Create a dictionary for each word
            word_dict = {'id': word_id,
                         'german': ger_word, 'english': eng_word}
            my_words.append(word_dict)

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"Error: {e}")

    return my_words


def save_vocab_to_json(vocab, filepath):
    """
    Saves a list of vocabularies to a JSON file.

    Args:
        vocab (list): List of vocabularies to be saved.
        filepath (str): Path of the JSON file where the vocabularies will be saved.
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(vocab, file, ensure_ascii=False, indent=4)


# Specify the paths of the vocabulary and JSON files
vocab_txt_file = "data/my_vocab.txt"
vocab_json_file = "my_words.json"

# Convert the vocabulary file to a list of dictionaries
my_words = convert_txt_to_vocab_list(vocab_txt_file)

# Save the list of dictionaries to a JSON file
save_vocab_to_json(my_words, vocab_json_file)
