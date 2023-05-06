import json


def save_vocab_to_json(vocab, filepath):
    """
    Save a vocabulary list to a JSON file

    :param vocab: A list of dictionaries containing word information.
    :param filepath: The file path where the JSON file will be saved.
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(vocab, file, ensure_ascii=False, indent=4)


def convert():
    """
    Read a vocabulary text file and convert it to a list of dictionaries
    :return: A list of dictionaries containing word information.
    """
    my_words = []

    with open("data/my_vocab.txt", "r", encoding="utf-8") as f:
        content = f.read()

    splitcontent = content.splitlines()
    adjusted_content = [x.replace("\t", " : ").replace('.', '')
                        for x in splitcontent]

    for i, word in enumerate(adjusted_content):

        # Skip empty lines
        if not word.strip():
            continue

        word_id = i + 1
        eng_word, ger_word = word.split(" : ")

        word_dict = {'id': word_id, 'german': ger_word,
                     'english': eng_word}
        my_words.append(word_dict)

    return my_words


my_words = convert()
save_vocab_to_json(my_words, "my_words.json")
