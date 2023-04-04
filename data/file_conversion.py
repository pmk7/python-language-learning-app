my_words = []

def convert():
    f = open("data/my_vocab.txt", "r", encoding="utf-8")
    content = f.read()
    f.close()
    splitcontent = content.splitlines()
  
    adjusted_content = [x.replace("\t", " : ").replace('.', '') for x in splitcontent]
    
    for i, word in enumerate(adjusted_content):
        word_id = i + 1
        eng_word, ger_word = word.split(" : ")
    
        word_dict = {'id': word_id, 'german': ger_word, 'english': eng_word, 'correct': 0, 'incorrect': 0}
        my_words.append(word_dict)
        
        
    return my_words
    


   
my_words = convert()    
