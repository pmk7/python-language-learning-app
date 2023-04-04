import json

output_file = 'my_vocab.json'
my_words = []


def line_to_dict(split_line):
    line_dict = {}
    for part in split_line:
        key, value = part.split(":")
        line_dict[key] = value

    return line_dict


def convert():
    f = open("my_vocab.txt", "r", encoding="utf-8")
    content = f.read()
    f.close()
    splitcontent = content.splitlines()
  
    adjusted_content = [x.replace("\t", " : ").replace('.', '') for x in splitcontent]
    
    for i, word in enumerate(adjusted_content):
        word_id = i + 1
        eng_word, ger_word = word.split(" : ")
    
        word_dict = {'id': word_id, 'german': ger_word, 'english': eng_word, 'correct': 0, 'incorrect': 0}
        my_words.append(word_dict)
        
        
    

    
    words_json = json.dumps((my_words), ensure_ascii=False)
    print(words_json)
    
    
   
    
    
convert()