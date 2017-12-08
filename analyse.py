# encoding:utf-8
import csv
import collections
import math
import os
import shutil
import numpy as np
from operator import itemgetter

from messages import Messages
from document import Document, DocumentStatistics
from group import Group
from utils import Linker, FileMaker

def do_analyse():
    linker = Linker("assets.rudevs.ru/experiments/too-broad-analysis", "http")
    prefix = "assets"
    question_folder = "%s/%s" % (prefix, Linker.question_folder)
    group_folder = "%s/%s" % (prefix, Linker.group_folder)
    we_use = 10 # How many answers there will be in the meta post

    if os.path.exists(prefix):
        shutil.rmtree(prefix)

    os.makedirs(question_folder)
    os.makedirs(group_folder)

    documents = parse_question_file(linker)
    Messages.on_parsed()

    stat = DocumentStatistics(documents)
    Messages.on_stat_ready()

    stat.vectorise_documents()
    Messages.on_doc_vectorised()

    similar = stat.similar_documents()
    similar = [item for item in similar if len(item) > 1]
    Messages.biggest_class_lenght(np.amax([len(value) for value in similar]))
    Messages.docs_classes_stat(len(documents), len(similar))

    lengths = {index: len(value) for index, value in enumerate(similar)}
    final_classes = [key for key, _ in sorted(lengths.items(), key=itemgetter(1), reverse=True)]

    groups = [Group(index, similar[index], linker) for index in final_classes]
    files = [FileMaker(group, group_folder) for group in groups]
    files.extend([FileMaker(document, question_folder) for document in documents])

    for file in files:
        file.dump()

    for answer in groups[:we_use]:
        Messages.send_to_output(str(answer))

def parse_question_file(linker, filename="questions.csv"):
    result = list()
    with open(filename, 'rt', encoding="utf8") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            question_id, title, body, tags, score, user_id = row
            try:
                question_id = int(question_id)
                user_id = int(user_id)
            except:
                continue

            result.append(Document(question_id, title, body, tags, score, user_id, linker))

    return result
    