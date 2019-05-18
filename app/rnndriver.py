from textgenrnn import textgenrnn


#textgen.generate_samples(max_gen_length=140)
#textgen.generate(max_gen_length=140)
#textgen.generate_to_file('textgenrnn_texts.txt', max_gen_length=140)

def generateLhTweet():
    textgen = textgenrnn(weights_path='lambhoot_weights.hdf5',
        vocab_path='lambhoot_vocab.json',
        config_path='lambhoot_config.json')
    return textgen.generate(max_gen_length=140, n=1, return_as_list=True)[0]

#text = generateLhTweet()
#print("the text is " + text[0])