# encoding:utf-8
import sys
import os

class Messages:
    parsing_completed   = "Parsing question file completed"
    stat_ready          = "Statistics is ready"
    vectorized          = "Docs vectorised"

    # Meta Post's Strings    
    group_number = u"Группа №"
    auto_warning = u"**Внимание!** Это автоматически созданный ответ, пожалуйста, не вносите в него правки."

    @staticmethod
    def start_msg():
        return "==================="

    @staticmethod
    def end_msg():
        return "==================="

    @staticmethod
    def endl():
        return "\r\n"

    @staticmethod
    def send_to_output(msg):
        print(msg)

    @staticmethod
    def default_msg(msg):
        return "%s%s%s%s" % (Messages.start_msg(), msg, Messages.end_msg(), Messages.endl())

    @staticmethod
    def on_parsed():
        Messages.send_to_output(Messages.default_msg(Messages.parsing_completed))

    @staticmethod
    def on_stat_ready():
        Messages.send_to_output(Messages.default_msg(Messages.stat_ready))

    @staticmethod
    def on_doc_vectorised():
        Messages.send_to_output(Messages.default_msg(Messages.vectorized))    

    @staticmethod    
    def biggest_class_lenght(lenght):
        msg  = "Biggest class has lenght %s" % (str(lenght)) 
        Messages.send_to_output(Messages.default_msg(msg))  

    @staticmethod    
    def docs_classes_stat(docs, classes):
        msg = "Documents %s; classes: %s" % (str(docs), str(classes))
        Messages.send_to_output(Messages.default_msg(msg))

    @staticmethod
    def meta_post_header(number):
        msg = "%s%s  %s%s" % (Messages.group_number, str(number), Messages.endl(), Messages.endl())
        return msg

    @staticmethod
    def meta_post_item(title, link):
        msg = " - [%s](%s) %s" % (title, link, Messages.endl())
        return msg

    @staticmethod
    def meta_post_warning():
        msg = "%s%s%s  %s" % (Messages.endl(), Messages.endl(), Messages.auto_warning, Messages.endl())
        return msg