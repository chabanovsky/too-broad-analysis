# encoding:utf-8
import csv
import collections
import math
import numpy as np
from operator import itemgetter

from utils import process_text, build_dataset
from messages import Messages

class Document:
    def __init__(self, question_id, title, body, tags, score, user_id, linker):
        self.question_id = question_id
        self.title  = title
        self.body   = body
        self.tags   = " ".join(tags.split("|"))
        self.score  = score
        self.user_id = user_id
        self.filtered_text = "%s %s %s" % (process_text(self.body), process_text(self.title), self.tags)
        self.tfs    = self.process_tf()
        self.linker = linker

    def process_tf(self):
        text = self.filtered_text
        words = collections.Counter(text).most_common()
        total_count = sum([count for word, count in words])
        return {word: float(count)/float(total_count) for word, count in words}

    def contains(self, word):
        return self.tfs.get(word, None) != None

    def vectorise(self, vector_proto):
        result = list()
        for word, idf in vector_proto:
            if self.contains(word):
                w = self.tfs[word]
                result.append(w * idf)
            else:
                result.append(0.)
        self.vector = np.zeros((1, len(result)))
        self.vector[0] = np.array(result)
        

    def cosine(self, other):
        norms = float(np.linalg.norm(self.vector) * np.linalg.norm(other.vector))
        if norms != 0.:
            val = self.vector.dot(other.vector.transpose()) / norms
            return float(val[0][0])
        else:
            return 0

    def common_vector(self, vector):
        return self.vector * vector

    def __str__(self):
        output = "%s%s" % (self.title, Messages.endl())
        output += "%s%s%s%s" % (Messages.start_msg(), Messages.end_msg(), Messages.endl(), Messages.endl())
        output += "%s%s" % (self.body , Messages.endl())
        output += "%s%s%s%s" % (Messages.start_msg(), Messages.end_msg(), Messages.endl(), Messages.endl())
        output += "%s%s%s" % (self.tags , Messages.endl(), Messages.endl())
        output += "https://ru.stackoverflow.com/q/%s" % (str(self.question_id))

        return output

    def filename(self):
        return "%s.%s" % (str(self.question_id), self.linker.ext())

class DocumentStatistics:
    def __init__(self, documents):
        self.documents = documents
        self.N = len(documents)

        self.full_text = " ".join([doc.filtered_text for doc in self.documents])
        indexes, dataset, word_to_index, index_to_word = build_dataset(self.full_text)

        self.word_indexes = indexes
        # Three following fields should be of the same size.
        self.dataset = dataset
        self.word_to_index = word_to_index
        self.index_to_word = index_to_word

        self.idfs = self.process_idf()

    def process_idf(self):
        result = dict()
        for word, count in self.dataset:
            document_with_word_count = float(sum([1 for document in self.documents if document.contains(word)]))
            if document_with_word_count != 0.:
                result[word] = math.log(float(self.N)/document_with_word_count, 10)
            else:
                Messages.send_to_output(Messages.something_went_wrong("|D with word| is 0, word '%s'" % (word)))
                result[word] = 1

        return result

    def vector_proto(self):
        vector = [(self.index_to_word[key], self.idfs[self.index_to_word[key]]) for key in sorted(self.index_to_word)]
        return vector

    def empty_vector_proto(self):
        return np.zeros((1, len(self.dataset))) + 1

    def vector_to_words(self, vector):
        vector = vector[0].tolist()
        return [self.index_to_word[index] for index, weight in enumerate(vector) if weight != 0.]

    def vectorise_documents(self):
        proto = self.vector_proto()
        for document in self.documents:
            document.vectorise(proto)

    def similar_documents(self, threshold=0.91):
        def lowest_cosine(cosines, document, threshold):
            closest = threshold
            result_index = -1
            lenght = len(cosines)
            for index in range(0, lenght):
                current_set = cosines[index]
                curr_closest = threshold
                curr_threshold = 1.
                
                for item in current_set:
                    cosin = abs(item.cosine(document))
                    if cosin > curr_closest:
                        curr_closest = cosin
                    if cosin < curr_threshold:
                        curr_threshold = cosin
                        
                if curr_closest > closest and curr_threshold >= threshold:
                    closest = curr_closest
                    result_index = index

            return result_index
        
        result = list()    
        for document in self.documents:
            index = lowest_cosine(result, document, threshold)
            if index < 0:
                result.append([document])
            else:
                result[index].append(document)
        
        return result
