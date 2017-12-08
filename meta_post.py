# encoding:utf-8
import sys
import os

from messages import Messages

class Group:
    def __init__(self, id, similar, linker):
        self.id = id
        self.similar = similar
        self.linker = linker
    
    def __str__(self):
        output = Messages.meta_post_header(self.id)
        for item in self.similar:
            output += Messages.meta_post_item(item.title, self.similar_questin_link(item))
        output += Messages.meta_post_warning()

        return output

    def similar_questin_link(self, question):
        return self.linker.question_url(question.question_id)

    def filename(self):
        return "%s.%s" % (self.id, self.linker.ext())
