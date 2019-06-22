from textgenrnn import textgenrnn
from datetime import datetime
import os


class RnnService:
    # default values
    weights_path='lambhoot_weights.hdf5'
    vocab_path='lambhoot_vocab.json'
    config_path='lambhoot_config.json'

    textgen = textgenrnn(weights_path=weights_path,
        vocab_path=vocab_path,
        config_path=config_path)

#textgen.generate_samples(max_gen_length=140)
#textgen.generate(max_gen_length=140)
#textgen.generate_to_file('textgenrnn_texts.txt', max_gen_length=140)

    def loadTextgen(self, weights_path, vocab_path, config_path):
        self.weights_path = weights_path
        self.vocab_path = vocab_path
        self.config_path = config_path
        self.textgen = textgenrnn(weights_path=weights_path,
            vocab_path=vocab_path,
            config_path=config_path)

    def generateLhTweet(self, max_length, temp):
        generated = self.textgen.generate(max_gen_length=140, temperature=temp, n=1, return_as_list=True)
        return generated[0]

    def buildModel(self, inputFilePath, modelName):
        train_cfg, model_cfg = self.getModelConfig()

        file_name = inputFilePath #"logs/twitter_log_text.txt"
        model_name = modelName #'twitter_log_text'   # change to set file name of resulting trained models/texts
        textgen = textgenrnn(name=model_name)

        self.trainModel(train_cfg, textgen, file_name, model_cfg)

    def trainModel(self, train_cfg, textgen, file_name, model_cfg):
        train_function = textgen.train_from_file if train_cfg['line_delimited'] else textgen.train_from_largetext_file

        train_function(
            file_path=file_name,
            new_model=True,
            num_epochs=train_cfg['num_epochs'],
            gen_epochs=train_cfg['gen_epochs'],
            batch_size=1024,
            train_size=train_cfg['train_size'],
            dropout=train_cfg['dropout'],
            validation=train_cfg['validation'],
            is_csv=train_cfg['is_csv'],
            rnn_layers=model_cfg['rnn_layers'],
            rnn_size=model_cfg['rnn_size'],
            rnn_bidirectional=model_cfg['rnn_bidirectional'],
            max_length=model_cfg['max_length'],
            dim_embeddings=100,
            word_level=model_cfg['word_level'])

    def getModelConfig(self):
        model_cfg = {
            'word_level': True,   # set to True if want to train a word-level model (requires more data and smaller max_length)
            'rnn_size': 200,   # number of LSTM cells of each layer (128/256 recommended)
            'rnn_layers': 6,   # number of LSTM layers (>=2 recommended)
            'rnn_bidirectional': True,   # consider text both forwards and backward, can give a training boost
            'max_length': 10,   # number of tokens to consider before predicting the next (20-40 for characters, 5-10 for words recommended)
            'max_words': 1000000000,   # maximum number of words to model; the rest will be ignored (word-level model only)
        }

        train_cfg = {
            'line_delimited': True,   # set to True if each text has its own line in the source file
            'num_epochs': 20,   # set higher to train the model for longer
            'gen_epochs': 1,   # generates sample text from model after given number of epochs
            'train_size': 1.0,   # proportion of input data to train on: setting < 1.0 limits model from learning perfectly
            'dropout': 0.1,   # ignore a random proportion of source tokens each epoch, allowing model to generalize better
            'validation': False,   # If train__size < 1.0, test on holdout dataset; will make overall training slower
            'is_csv': False   # set to True if file is a CSV exported from Excel/BigQuery/pandas
        }
        return train_cfg, model_cfg

#buildModel()

#generateLhTweet()

#text = generateLhTweet()
#print("the text is " + text[0])