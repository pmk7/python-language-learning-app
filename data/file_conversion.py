import json


def read_vocab_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.readlines()
    return content


def convert_txt_to_vocab_list(filepath):
    my_words = []

    try:
        content = read_vocab_file(filepath)
        adjusted_content = [x.strip().replace(
            "\t", " : ").replace('.', '') for x in content]

        for i, word in enumerate(adjusted_content):
            if not word.strip():
                continue

            word_id = i + 1
            eng_word, ger_word = word.split(" : ")

            word_dict = {'id': word_id, 'german': ger_word,
                         'english': eng_word}
            my_words.append(word_dict)

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"Error: {e}")

    return my_words


def save_vocab_to_json(vocab, filepath):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(vocab, file, ensure_ascii=False, indent=4)


vocab_txt_file = "data/my_vocab.txt"
vocab_json_file = "my_words.json"

my_words = convert_txt_to_vocab_list(vocab_txt_file)
save_vocab_to_json(my_words, vocab_json_file)
