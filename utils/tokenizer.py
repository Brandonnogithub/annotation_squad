import re
import json
import collections
import stanza
from config import config

####################################################
# Here we provide three different tokenizer
# 1. stanford tokenizer, which is the best maybe
# 2. nltk tokenizer, which is easy to use (not impelement yet since stanford's is good enough)
# 3. Bert tokenizer, which is the most simple
####################################################


def load_vocab(vocab_file):
    """Loads a vocabulary file into a dictionary."""
    vocab = collections.OrderedDict()

    with open(vocab_file, "r", encoding="utf-8") as reader:
        while True:
            token = reader.readline()
            if not token:
                break
            idx, token, _ = token.strip().split("\t")
            vocab[token] = int(idx)

    return vocab


class Indexer(object):
    def __init__(self, vocab_path=None):
        super(Indexer, self).__init__()
        if not vocab_path:
            vocab_path = config.vocab_path

        self.vocab = load_vocab(vocab_path)
        self.ids_to_tokens = collections.OrderedDict([(ids, tok) for tok, ids in self.vocab.items()])

    def convert_tokens_to_ids(self, tokens):
        """Converts a sequence of tokens into ids using the vocab."""
        ids = []
        for token in tokens:
            ids.append(self.vocab[token])
        return ids     

    def convert_ids_to_tokens(self, ids):
        tokens = []
        for id in ids:
            tokens.append(self.ids_to_tokens[id])
        return tokens



class BaseTokenizer(object):
    "basic tokenizer class"
    def __init__(self):
        super(BaseTokenizer, self).__init__()

    def tokenize(self, context):
        '''
        context:   str
        return: token list
        '''
        return []

    
class WhitespaceTokenizer(BaseTokenizer):
    def __init__(self):
        super(WhitespaceTokenizer, self).__init__()

    def tokenize(self, context):
        context = context.strip()
        if not context:
            return []
        tokens = context.split(" ")
        return tokens


class StanfordTokenizer(BaseTokenizer):
    def __init__(self, processors="tokenize,pos", verbose=False, use_gpu=True):
        super(StanfordTokenizer, self).__init__()

        # this model will use gpu to process sentences (abuot 1.3G memory for all processors)
        try:
            self.nlp = stanza.Pipeline('en', processors=processors, verbose=verbose, use_gpu=use_gpu)    
        except:
            stanza.download("en")
            self.nlp = stanza.Pipeline('en', processors=processors, verbose=verbose, use_gpu=use_gpu) 

        self.doc = None     # record last process result
        self.idx_pattern = re.compile(r'\d+')

    def tokenize(self, context):
        '''
        word {
            "id": "1",
            "text": "footbal",
            "upos": "NOUN",
            "xpos": "NN",
            "misc": "start_char=0|end_char=8"
        }
        '''
        self.doc = self.nlp(context)
        return [word.text for sentence in self.doc.sentences for word in sentence.words]


    def character_level_idx(self, context=None):
        '''
        return character_level index of context, if context is None, use last result
        '''
        if context:
            pass    # to be implement
        else:
            return [[int(i) for i in self.idx_pattern.findall(word.misc)] for sentence in self.doc.sentences for word in sentence.words]


def test_tokenizer():
    s = "I like playing football(a $ sport)."
    tokenizer = StanfordTokenizer()
    tokenizer.tokenize(s)
    res = tokenizer.character_level_idx()
    print(res)


if __name__ == "__main__":
    test_tokenizer()
