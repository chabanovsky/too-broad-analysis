# encoding:utf-8
import re
import nltk
import pymorphy2
import collections

morph = pymorphy2.MorphAnalyzer()

def filter_noise(text):
    text = re.sub('<pre>.*?</pre>',' ', text, flags=re.DOTALL)
    text = re.sub('<code>.*?</code>',' ', text, flags=re.DOTALL)
    text = re.sub('<[^<]+?>', ' ', text, flags=re.DOTALL) 
    text = re.sub('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', ' ', text, flags=re.DOTALL)             
    text = re.sub('(https|http)?:\/\/.*', '', text)
    return text

def process_text(text, extended_filter=False, word_len_threshold=2):
    global morph

    def process(filter, token, word_len_threshold):
        global morph

        p = morph.parse(token)[0]
        if len(p.normal_form) < word_len_threshold:
            return None
        
        # http://pymorphy2.readthedocs.io/en/latest/user/grammemes.html
        if any(tag in str(p.tag) for tag in ['PNCT', 'NUMB', 'UNKN']): # ['LATN', 'PNCT', 'NUMB', 'UNKN']
            return None
        # http://pymorphy2.readthedocs.io/en/latest/user/grammemes.html
        if str(p.tag.POS) not in filter:
            return  str(p.normal_form)  

    otput_data = ""
    if extended_filter:
        filter = ['PREP']
    else:    
        filter = ['NPRO', 'PREP', 'PRED', 'CONJ', 'PRCL', 'INTJ']

    text = filter_noise(text)
    text = text.lower()

    sent_text = nltk.sent_tokenize(text)
    for sentence in sent_text:
        tokenized_text = nltk.word_tokenize(sentence)
        for token in tokenized_text:
            
            token = token.replace('.', ' ')
            token = token.replace('/', ' ')

            for sub_token in token.split():
                processed = process(filter, sub_token, word_len_threshold)
                if processed is not None:
                    otput_data += " " + processed
        
    return otput_data


def build_dataset(words, n_words=None):
    count = [['UNK', -1]]
    count.extend(collections.Counter(words).most_common(n_words))
    dictionary = dict()
    for word, _ in count:
        dictionary[word] = len(dictionary)
    data = list()
    unk_count = 0
    for word in words:
        if word in dictionary:
            index = dictionary[word]
        else:
            index = 0  # dictionary['UNK']
            unk_count += 1
        data.append(index)
    count[0][1] = unk_count
    reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return data, count, dictionary, reversed_dictionary


class Linker:
    group_folder    = "groups"
    question_folder = "questions"

    def __init__(self, base_url, protocol="https", file_ext="txt"):
        self.base_url = base_url
        self.protocol = protocol
        self.file_ext = file_ext

    def question_url(self, question_id):
        return "%s/%s.%s" % (self.questions_url(), str(question_id), self.file_ext)

    def group_url(self, group_id):
        return "%s/%s.%s" % (self.groups_url(), str(group_id), self.file_ext)

    def groups_url(self):
        return "%s://%s/%s" % (self.protocol, self.base_url, Linker.group_folder)

    def questions_url(self):
        return "%s://%s/%s" % (self.protocol, self.base_url, Linker.question_folder)

    def ext(self):
        return self.file_ext

class FileMaker:
    def __init__(self, item, prefix="data"):
        self.item = item
        self.prefix = prefix

    def dump(self):
        filename = "%s/%s" % (self.prefix, self.item.filename())
        with open(filename, 'w') as file:
            file.write(str(self.item))